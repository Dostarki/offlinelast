"""Live admin API smoke for zombie_count PUT via public preview URL.

Admin login requires Origin header equal to ADMIN_PROXY_ORIGIN.
Admin password per repo: 123123.
"""
import os
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://utility-15.preview.emergentagent.com').rstrip('/')
# Public ingress (Cloudflare worker) rewrites Origin to an internal preview host
# before forwarding; that forwarded Origin is NOT in ADMIN_PROXY_ORIGIN, which
# breaks admin login through the public URL in this preview environment. Backend
# tests therefore target the internal admin API directly where the real Origin is
# preserved. (See report: live admin login via public preview URL returns 403.)
INTERNAL_URL = 'http://localhost:8001'
ORIGIN = 'https://utility-15.preview.emergentagent.com'


def _login():
    s = requests.Session()
    s.headers.update({'Origin': ORIGIN, 'Content-Type': 'application/json'})
    r = s.post(f'{INTERNAL_URL}/api/admin/login', json={'password': '123123'}, timeout=10)
    assert r.status_code == 200, f'login failed: {r.status_code} {r.text}'
    # Cookies are set with secure=True; requests won't resend them over http://.
    # Rebuild a plain cookie jar from the Set-Cookie values so follow-up calls work.
    cookies = {}
    for name in ('admin_access', 'admin_refresh'):
        val = r.cookies.get(name)
        if val:
            cookies[name] = val
    s.cookies.clear()
    for name, val in cookies.items():
        s.cookies.set(name, val, path='/api/admin')
    return s


def test_admin_status_includes_zombies_field():
    s = _login()
    r = s.get(f'{INTERNAL_URL}/api/admin/status', timeout=10)
    assert r.status_code == 200, r.text
    data = r.json()
    for k in ('humans', 'bots', 'total', 'zombies', 'tick_ms', 'participants'):
        assert k in data, f'missing {k}'
    assert isinstance(data['zombies'], int)
    assert isinstance(data['tick_ms'], (int, float))


def test_admin_settings_put_zombie_count():
    s = _login()
    # Read current
    r = s.get(f'{INTERNAL_URL}/api/admin/settings', timeout=10)
    assert r.status_code == 200, r.text
    settings = r.json()
    assert 'zombie_count' in settings and 'zombie_density' in settings

    # Set to a specific count
    new = dict(settings)
    new['zombie_density'] = 'normal'
    new['zombie_count'] = 75
    r = s.put(f'{INTERNAL_URL}/api/admin/settings', json=new, timeout=10)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body['zombie_count'] == 75

    # Verify via GET
    r = s.get(f'{INTERNAL_URL}/api/admin/settings', timeout=10)
    assert r.json()['zombie_count'] == 75

    # Reject out-of-range
    bad = dict(new); bad['zombie_count'] = 999
    r = s.put(f'{INTERNAL_URL}/api/admin/settings', json=bad, timeout=10)
    assert r.status_code in (400, 422), f'expected validation error, got {r.status_code}'

    # Reject non-int (strict)
    bad2 = dict(new); bad2['zombie_count'] = 50.5
    r = s.put(f'{INTERNAL_URL}/api/admin/settings', json=bad2, timeout=10)
    assert r.status_code in (400, 422)

    # Density off => target 0 (status reflects after population loop clears)
    off = dict(new); off['zombie_density'] = 'off'; off['zombie_count'] = 0
    r = s.put(f'{INTERNAL_URL}/api/admin/settings', json=off, timeout=10)
    assert r.status_code == 200
    assert r.json()['zombie_count'] == 0

    # Restore to a reasonable default so we don't leave the server empty
    restore = dict(new); restore['zombie_density'] = 'normal'; restore['zombie_count'] = 250
    r = s.put(f'{INTERNAL_URL}/api/admin/settings', json=restore, timeout=10)
    assert r.status_code == 200


def test_admin_login_requires_origin():
    s = requests.Session()
    s.headers.update({'Content-Type': 'application/json'})  # no Origin
    r = s.post(f'{INTERNAL_URL}/api/admin/login', json={'password': '123123'}, timeout=10)
    assert r.status_code == 403, f'expected 403 w/o origin, got {r.status_code}'
