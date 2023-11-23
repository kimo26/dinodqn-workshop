from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import base64
from time import sleep

class Game:
    def __init__(self):
        game_url = 'chrome://dino'

        options = Options()
        options.add_argument('disable-infobars')
        options.add_argument('--mute-audio')
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.action_chains = ActionChains(self.driver)

        try:
            self.driver.get(game_url)
        except WebDriverException:
            pass

        sleep(2)
        self.jump()
        sleep(3)

        self.fig, self.ax = plt.subplots()
        self.image = None

        self.getScreen()
        sleep(10)

    def jump(self):
        self.action_chains.key_down(Keys.ARROW_UP).perform()

    def show(self, img):
        if self.image is None:
            self.image = self.ax.imshow(img, animated=True)
        else:
            self.image.set_data(img)

        plt.draw()
        plt.pause(0.033)  # Approximately 30fps

    def getScreen(self, debug=True):
        leading = len('data:image/png;base64,')
        canvas = 'document.querySelector("#main-frame-error > div.runner-container > canvas")'
        img = self.driver.execute_script(f'return {canvas}.toDataURL();')

        img = img[leading:]
        img = np.array(Image.open(BytesIO(base64.b64decode(img))))

        if debug:
            self.show(img)

        return img

g = Game()
try:
    while True:
        g.getScreen()
finally:
    g.driver.quit()
