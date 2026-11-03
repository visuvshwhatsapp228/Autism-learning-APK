# Build the Android APK with GitHub Actions

This project contains source code, not a prebuilt APK. The included workflow
builds a debug APK in GitHub's Ubuntu runner.

## Steps

1. Create a new GitHub repository.
2. Upload the *contents* of this project folder to the repository (the
   `.github/workflows/android-apk.yml` file must be included).
3. Open the repository's **Actions** tab.
4. Select **Build Android APK** and choose **Run workflow**. A push to
   `main` or `master` also starts a build automatically.
5. When the run finishes successfully, open that run and download the
   `autism-learning-android-apk` artifact.
6. Extract the artifact and install the `.apk` on the Android tablet.
   You may need to allow installation from that file manager/browser.

## Important

- The workflow creates a **debug APK** for testing, not a Play Store release.
- Android may show a warning because this APK is not signed with a
  Play Store release key.
- The APK is not available until the GitHub Actions build completes.
- If the build fails, open the failed Actions run and share its log so the
  build configuration can be corrected.
