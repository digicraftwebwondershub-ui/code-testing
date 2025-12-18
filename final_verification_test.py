import asyncio
import os
from playwright.async_api import async_playwright, expect

async def main():
    """
    This script serves as a smoke test to visually verify that the application
    loads successfully after the backend fixes have been applied. It does not
    mock any backend calls, relying on the live Google Apps Script environment.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Listen for console messages and page errors to aid debugging if the test fails.
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))

        # Construct the absolute path to the local HTML file.
        file_path = f"file://{os.getcwd()}/Index.html"
        await page.goto(file_path)

        print("Waiting for the application to load...")

        # We will wait up to 20 seconds for the main application view to become visible.
        # This gives the live backend enough time to respond.
        app_view = page.locator("#app-view")

        try:
            # The main verification step:
            # Does the app view become visible, indicating a successful login and data load?
            await expect(app_view).to_be_visible(timeout=20000)
            print("Verification successful: The main application view is visible.")
        except Exception as e:
            print(f"Verification failed: The app view did not become visible within the timeout. Error: {e}")
            print("The application may still be stuck on the 'Authenticating...' screen.")

        # Take a screenshot regardless of success or failure for manual inspection.
        screenshot_path = "./verification_artefacts/final_verification.png"
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot captured and saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    # Create the verification directory if it doesn't exist
    os.makedirs("/home/jules/verification", exist_ok=True)
    asyncio.run(main())
