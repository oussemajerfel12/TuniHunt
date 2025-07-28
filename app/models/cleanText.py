import re
class clean:
    def __init__(self,text):
        self.text= text
    
    def clean_text(self):
        string = re.sub(r'[?|\$|\.|!]', '', self.text)
        cleand_string = re.sub(r'\n{1,}','.',string)
        return cleand_string
    
    def extend_Numero(self):
        match = re.search(r'\b\d{8}\b',self.text)
        if match:
            return match.group(0)
        return None
