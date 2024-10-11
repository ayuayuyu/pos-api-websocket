from typing import List,Dict

class filter:
    def __init__(self):
        self.count = 0
        #複数の端末情報を管理するために辞書をしようする
        self.keys: Dict[str, str] = {}
        
        def setCount(self):
            self.count = self.count+1
        
        def getCount(self):
            return self.count