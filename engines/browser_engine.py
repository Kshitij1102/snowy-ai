from playwright.sync_api import sync_playwright


# 🌐 OPEN BLINKIT + SEARCH + ADD TO CART
def open_blinkit(items):

    with sync_playwright() as p:

        browser = p.chromium.launch(

            headless=False,
            slow_mo=800

        )

        page = browser.new_page()

        # 🌐 OPEN BLINKIT
        page.goto(
            "https://blinkit.com"
        )

        # ⏳ WAIT FOR PAGE LOAD
        page.wait_for_timeout(6000)

        # 🔍 SEARCH + ADD LOOP
        for item in items:

            try:

                print(f"🛒 Processing item: {item}")

                # 🔍 SEARCH BAR
                search_box = page.locator(
                    'input[placeholder*="Search"]'
                ).first

                # CLICK SEARCH
                search_box.click()

                page.wait_for_timeout(1000)

                # CLEAR OLD SEARCH
                search_box.fill("")

                page.wait_for_timeout(500)

                # TYPE ITEM
                search_box.type(item)

                print(f"🔍 Searching: {item}")

                # ⏳ WAIT FOR RESULTS
                page.wait_for_timeout(5000)

                # 🛒 ADD BUTTON
                add_button = page.locator(
                    'button:has-text("ADD")'
                ).first

                # CLICK ADD
                add_button.click()

                print(
                    f"🛒 Verifying cart update for {item}"
                )

                page.wait_for_timeout(3000)

                print(f"✅ Added: {item}")

                page.wait_for_timeout(3000)

            except Exception as e:

                print(
                    f"❌ Failed for {item}:",
                    e
                )

        print("🛒 Cart preparation complete.")

        # ⏳ KEEP OPEN
        page.wait_for_timeout(20000)

        browser.close()