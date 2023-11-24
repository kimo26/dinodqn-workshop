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
import cv2

class Game:
    def __init__(self,debug = True):
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
        
        if debug:
            self.fig, self.ax = plt.subplots()
            self.image = None

        

    def jump(self):
        javascript = '''
            var event = new KeyboardEvent('keydown',{
                key: ' ',
                code: 'Space',
                keyCode : 32,
                charCode : 32,
                which : 32
            });
            document.dispatchEvent(event);
        '''
        self.driver.execute_script(javascript)

    def getScore(self):
        javascript = '''
            return Runner.instance_.distanceMeter.digits;
        '''
        raw_score = self.driver.execute_script(javascript)
        score = int(''.join(raw_score))
        return score
    def isGameOver(self):
        javascript = '''
            return Runner.instance_.crashed;
        '''
        crashed = self.driver.execute_script(javascript)
        return crashed
    def show(self, img):
        cv2.imshow('Game Screen', img)
        cv2.waitKey(1)
    def restart(self):
        javascript = '''
            Runner.instance_.restart();
        '''
        self.driver.execute_script(javascript)
        sleep(0.2)
        return True
    def getScreen(self, debug=True):
        leading = len('data:image/png;base64,')
        canvas = 'document.querySelector("#main-frame-error > div.runner-container > canvas")'
        img = self.driver.execute_script(f'return {canvas}.toDataURL();')

        img = img[leading:]
        img = np.array(Image.open(BytesIO(base64.b64decode(img))))[:,:,:3]
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #img = np.array(Image.fromarray(img).resize((250,100)))
        img = np.uint8(img)
        img = cv2.Canny(img,threshold1=120,threshold2=150)
        img = np.array(img)


        #print(img.shape) grayscale

        #print(np.max(img)) max val is 255
        if debug:
            self.show(img)

        #normalise - values normalise between 0 and 1
        img = img/255.
        return img

g = Game()
try:
    while True:
        g.getScreen()
        if g.isGameOver():
            g.restart()
        print(f'score: {g.getScore()}, is crashed: {g.isGameOver()}')
finally:
    g.driver.quit()
