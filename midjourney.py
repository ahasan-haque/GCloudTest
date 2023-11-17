import os
import asyncio
import json
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


# -------------------- SENSITIVE INFORMATION --------------------

load_dotenv(".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
DISCORD_EMAIL = os.getenv("DISCORD_EMAIL")
DISCORD_PASSWORD = os.getenv("DISCORD_PASSWORD")
PORT = os.getenv("PORT")

# --------------------------------------------------------------------------------

def automate_midjourney_slash_command(prompt):
    print("automating midjourney slash command")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()

        # Navigate to the Discord login page
        page = context.new_page()
        page.goto('https://discord.com/login')

        # Fill in the login form with your credentials
        page.fill('input[name="email"]', DISCORD_EMAIL)
        page.fill('input[name="password"]', DISCORD_PASSWORD)

        # Click the login button
        page.click('button[type="submit"]')

        # Wait for login to complete (you can modify this timeout)
        page.wait_for_selector('button[aria-label="User Settings"]')

        server_name = 'Midjourney Image Download Bot'
        try:
            page.click(f'div[aria-label*="{server_name}"]')
        except Exception as e:
            page.screenshot(path="example.png")
            page.locator('div:has-text("MIDB")').click()
        
        # Send a message to the general channel
        message = '/imagine'
        page.fill('div[role="textbox"]', message)

        page.click(f'div[id="autocomplete-0"]')
        page.fill('span[class^="optionPillValue"]', prompt)

        page.keyboard.press('Enter')

        import time;time.sleep(1)
        browser.close()
    return {"response": True}
