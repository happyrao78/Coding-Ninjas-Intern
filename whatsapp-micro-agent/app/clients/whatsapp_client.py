import os
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from app.config import settings

class WhatsAppClient: 
    def __init__(self):
        self.message_template = settings.custom_message
        self.driver = None
        self.is_initialized = False
        self.wait_time = 60  # seconds to wait for WhatsApp Web to load
        
    async def initialize(self):
        """Initialize WhatsApp Web with Selenium and load saved session if available"""
        try:
            # Set up Chrome options
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Create user data directory if it doesn't exist
            user_data_dir = os.path.abspath(settings.chrome_user_data_dir)
            os.makedirs(user_data_dir, exist_ok=True)
            
            # Set up Chrome to use a persistent user data directory
            options.add_argument(f"--user-data-dir={user_data_dir}")
            options.add_argument("--profile-directory=WhatsAppProfile")
            
            # Initialize Chrome driver
            self.driver = webdriver.Chrome(options=options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Open WhatsApp Web
            self.driver.get("https://web.whatsapp.com/")
            
            # Check if WhatsApp is already logged in
            try:
                # Wait for the search box to appear, which indicates we're logged in
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                )
                print("WhatsApp Web already logged in!")
                self.is_initialized = True
                return True
            except TimeoutException:
                # Not logged in yet, need to scan QR code
                print("Please scan the QR code within 60 seconds...")
                try:
                    WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                    )
                    print("WhatsApp Web logged in successfully!")
                    self.is_initialized = True
                    return True
                except TimeoutException:
                    print("Timeout waiting for WhatsApp Web to load. Please try again.")
                    self.driver.quit()
                    self.is_initialized = False
                    return False
                
        except Exception as e:
            print(f"Error initializing WhatsApp client: {e}")
            self.is_initialized = False
            return False
    
    async def send_message(self, phone, ngo_name):
        """Send WhatsApp message to the specified number using multiple methods"""
        if not self.is_initialized:
            success = await self.initialize()
            if not success:
                return {"success": False, "reason": "WhatsApp client not initialized"}
        
        try:
            # Format phone number (ensure it includes country code)
            phone = str(phone)
            if not phone.startswith("+"):
                # Assuming default country code is +91 (India)
                phone = f"+91{phone}" if not phone.startswith("91") else f"+{phone}"
                
            # Remove non-numeric characters except +
            phone = ''.join(filter(lambda x: x.isdigit() or x == '+', phone))
            
            # Format message with NGO name
            message = self.message_template.format(ngo_name=ngo_name)
            
            # URL encode the message to preserve formatting
            import urllib.parse
            encoded_message = urllib.parse.quote(message)
            
            # Open chat with the contact
            self.driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}")
            
            # Wait for the page to load completely
            time.sleep(5)
            
            # Try multiple methods to send the message
            success = await self._try_send_methods(phone, message)
            
            if success:
                print(f"Message sent successfully to {phone}")
                return {"success": True}
            else:
                return {"success": False, "reason": "Failed to send message with all methods"}
                
        except Exception as e:
            print(f"Error sending WhatsApp message to {phone}: {e}")
            return {"success": False, "reason": str(e)}
    
    async def _try_send_methods(self, phone, message):
        """Try multiple methods to send the message"""
        
        # Method 1: Try clicking send button with different selectors
        send_button_selectors = [
            '//span[@data-icon="send"]',
            '//button[@aria-label="Send"]',
            '//div[@aria-label="Send"]//span[@data-icon="send"]',
            '//span[@data-testid="send"]',
            '//*[@data-icon="send"]',
            '//button[contains(@class, "send")]//span[@data-icon="send"]'
        ]
        
        for selector in send_button_selectors:
            try:
                print(f"Trying selector: {selector}")
                send_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                
                # Scroll to button if needed
                self.driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
                time.sleep(1)
                
                # Try regular click
                send_button.click()
                time.sleep(2)
                
                # Check if message was sent by looking for the sent indicator
                if self._check_message_sent():
                    return True
                    
            except Exception as e:
                print(f"Method 1 failed with selector {selector}: {e}")
                continue
        
        # Method 2: Try JavaScript click
        try:
            print("Trying JavaScript click method...")
            send_button = self.driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            self.driver.execute_script("arguments[0].click();", send_button)
            time.sleep(2)
            
            if self._check_message_sent():
                return True
                
        except Exception as e:
            print(f"Method 2 (JavaScript click) failed: {e}")
        
        # Method 3: Try ActionChains
        try:
            print("Trying ActionChains method...")
            send_button = self.driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            actions = ActionChains(self.driver)
            actions.move_to_element(send_button).click().perform()
            time.sleep(2)
            
            if self._check_message_sent():
                return True
                
        except Exception as e:
            print(f"Method 3 (ActionChains) failed: {e}")
        
        # Method 4: Try Enter key on message input
        try:
            print("Trying Enter key method...")
            # Find message input box and press Enter
            message_input_selectors = [
                '//div[@contenteditable="true"][@data-tab="10"]',
                '//div[@contenteditable="true"][contains(@class, "message")]',
                '//div[@role="textbox"]'
            ]
            
            for input_selector in message_input_selectors:
                try:
                    message_input = self.driver.find_element(By.XPATH, input_selector)
                    message_input.click()
                    time.sleep(1)
                    message_input.send_keys(Keys.ENTER)
                    time.sleep(2)
                    
                    if self._check_message_sent():
                        return True
                        
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"Method 4 (Enter key) failed: {e}")
        
        # Method 5: Try PyAutoGUI as last resort
        try:
            print("Trying PyAutoGUI method...")
            send_button = self.driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            location = send_button.location_once_scrolled_into_view
            size = send_button.size
            
            # Calculate center of button
            x = location['x'] + size['width'] / 2
            y = location['y'] + size['height'] / 2
            
            # Get window position
            window_x = self.driver.execute_script("return window.screenX;")
            window_y = self.driver.execute_script("return window.screenY;")
            
            # Click using pyautogui
            pyautogui.click(window_x + x, window_y + y)
            time.sleep(2)
            
            if self._check_message_sent():
                return True
                
        except Exception as e:
            print(f"Method 5 (PyAutoGUI) failed: {e}")
        
        return False
    
    def _check_message_sent(self):
        """Check if message was successfully sent"""
        try:
            # Look for sent message indicators
            sent_indicators = [
                '//span[@data-icon="msg-check"]',  # Single check mark
                '//span[@data-icon="msg-dblcheck"]',  # Double check mark
                '//span[@data-icon="msg-dblcheck-ack"]',  # Blue double check mark
                '//*[contains(@class, "message-out")]'  # Outgoing message
            ]
            
            for indicator in sent_indicators:
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, indicator))
                    )
                    return True
                except TimeoutException:
                    continue
                    
            return False
            
        except Exception:
            return False
    
    async def disconnect(self):
        """Disconnect but keep session cookies"""
        if self.driver: 
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error disconnecting WhatsApp client: {e}")
        self.is_initialized = False