# CraftPanel `item` scope fix

- Fixed the weapon-recipe render crash by removing the out-of-scope equipment thumbnail.
- Added compact equipment thumbnails to the equipment crafting and owned-equipment upgrade card headers, where `item` is defined.
- `CI=true npx --no-install craco test CraftPanel.test.jsx --watchAll=false`: passed (1 suite, 1 test). Before the fix, the same test failed with `ReferenceError: item is not defined` at `CraftPanel.jsx:349`.
- `npx --no-install craco build`: completed. It retains existing optional Wagmi wallet connector resolution warnings.
