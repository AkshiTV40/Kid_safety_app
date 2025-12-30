# Android Build & Setup (Capacitor)

This file documents how to build the Android app using Capacitor.

Prerequisites:
- Node.js 20+, npm
- Java JDK 17
- Android SDK / Android Studio

Quick steps:
1. Install dependencies: npm ci
2. Export web assets: npm run build:web
3. Initialize Capacitor (only once): npx @capacitor/cli create
4. Add Android platform: npx cap add android
5. Sync web assets: npm run cap:sync
6. Open Android Studio: npm run cap:open:android
7. Create a signing key and configure signing in Android Studio
8. Build a signed AAB (Build > Generate Signed Bundle / APK > Android App Bundle)

CI notes:
- The GitHub Actions workflow will try to run `./gradlew bundleRelease` but you must provide signing keys as secrets and configure `android/gradle.properties` to use them.
- For production builds, configure keystore signing and set the upload key and app signing on Play Console.
