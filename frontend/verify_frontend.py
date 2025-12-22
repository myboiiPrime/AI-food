from playwright.sync_api import Page, expect, sync_playwright

def verify_app_navigation(page: Page):
    # Capture console logs
    page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
    page.on("pageerror", lambda err: print(f"Browser error: {err}"))

    # Navigate to the app's root URL
    print("Navigating to http://localhost:8081")
    page.goto("http://localhost:8081", timeout=30000)

    # Wait for the "Hello," text which is on the Hub screen.
    print("Waiting for 'Hello,' text...")
    hello_text = page.get_by_text("Hello,")
    expect(hello_text).to_be_visible(timeout=20000)

    # Check for "Snap & Cook" button
    snap_button = page.get_by_text("Snap & Cook")
    expect(snap_button).to_be_visible()

    # Check for "My Health Profile" button
    profile_button = page.get_by_text("My Health Profile")
    expect(profile_button).to_be_visible()

    # Take a screenshot of the Hub
    page.screenshot(path="/home/jules/verification/hub_screen.png")
    print("Hub screen verified.")

    # Navigate to Profile
    profile_button.click()

    # Wait for "Health Goals" text
    health_goals_text = page.get_by_text("Health Goals")
    expect(health_goals_text).to_be_visible()

    # Take a screenshot of Profile
    page.screenshot(path="/home/jules/verification/profile_screen.png")
    print("Profile screen verified.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_app_navigation(page)
            print("Verification successful!")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="/home/jules/verification/failure.png")
        finally:
            browser.close()
