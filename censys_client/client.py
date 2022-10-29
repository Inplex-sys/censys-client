
__version__ = "0.1.1"

import requests
import string
import colored
import random
import sys, os
import time
import argparse

__EXECDIR__ = os.path.dirname(os.path.realpath(__file__)) + ("\\" if os.name == "nt" else "/")

class Main:
    def genString( length ):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        pass
    
    def textHighlight( text ):
        return colored.stylize(text, colored.fg('wheat_1'), colored.attr('bold'))
        pass
    
    def textSuccess( text ):
        return colored.stylize(text, colored.fg('green'))
        pass

    def textDanger( text ):
        return colored.stylize(text, colored.fg('red'))
        pass
    
    def textPrimary( text ):
        return colored.stylize(text, colored.fg('cyan'))
        pass

class Setup:
    def getConfig():
        auths = []
        with open(__EXECDIR__ + 'config.txt', 'r') as file:
            lines = file.read().splitlines()
            if len(lines) == 0:
                print(f"{Main.textDanger('No')} API ID and API Secret found in {Main.textHighlight(__EXECDIR__ + 'config.txt')}")
                addOther = str(input("Would you like to add one ? (y/n): "))
                if addOther == 'y':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    Setup.config()
                sys.exit(0)
                pass
            for line in lines:
                auths.append((line.split(':')[0], line.split(':')[1]))
                pass
            file.close()
            pass

        return auths
        pass

    def config():
        username = str(input(f"Censys API ID {Main.textPrimary('(********************************98d1)')}: "))
        password = str(input(f"Censys API Secret {Main.textPrimary('(****************************aucc)')}: "))
        
        if username == '' or password == '':
            print(f"You have provided {Main.textDanger('unvalid')} Censys API ID and API Secret")
            addOther = str(input("Would you like to retry ? (y/n): "))
            if addOther == 'y':
                os.system('cls' if os.name == 'nt' else 'clear')
                Setup.config()
            sys.exit(0)
            pass

        with open(__EXECDIR__ + 'config.txt', 'a+') as file:
            lines = file.readlines()
            for line in lines:
                if username == line.split(':')[0]:
                    print("API ID and API Secret already set")
                    addOther = str(input("Would you like to retry ? (y/n): "))
                    if addOther == 'y':
                        os.system('cls' if os.name == 'nt' else 'clear')
                        Setup.config()
                    sys.exit(0)
                    pass
                pass
            pass

            if Censys.check( username, password ):
                file.write(f"{username}:{password}\n")
            else:
                print(f"This API ID and API Secret are {Main.textDanger('not registered')}")
                addOther = str(input("Would you like to retry ? (y/n): "))
                if addOther == 'y':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    Setup.config()
                sys.exit(0)
                pass
            file.close()
            pass
            
        print(f"Your API ID and API Secret have been {Main.textSuccess('successfully')} saved to {Main.textHighlight(__EXECDIR__ + 'config.txt')}")
        addOther = str(input("Would you like to add another API ID and API Secret ? (y/n): "))
        if addOther == 'y':
            os.system('cls' if os.name == 'nt' else 'clear')
            Setup.config()
        sys.exit(0)
        pass

class Censys:
    def __init__( self, auth, output ):
        self.auth = auth
        self.totalAuth = len(auth)
        self.totalCount = 0
        self.rawData = ''

        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100'
        }

        if output != None: 
            self.outputFile = output
        else: 
            self.outputFile = f'./result-{Main.genString(10)}.txt'
            pass

        self.quota = self.account()['quota']
        pass

    @staticmethod
    def check( username, password ):
        httpResponse = requests.get('https://search.censys.io/api/v1/account', headers={'Accept': 'application/json'}, auth=(username, password))
        if httpResponse.status_code == 200:
            return True
        else:
            return False
            pass
        pass

    def account( self, auth=False ):
        if not auth:
            httpResponse = {
                'quota': {
                    'used': 0,
                    'allowance': 0,
                }
            }

            for user, password in self.auth:
                response = requests.get('https://search.censys.io/api/v1/account', headers=self.headers, auth=(user, password)).json()
                if 'error' not in response.keys():
                    httpResponse['quota']['used'] += response['quota']['used']
                    httpResponse['quota']['allowance'] += response['quota']['allowance']
                    pass
                pass
            pass
        else:
            httpResponse = requests.get('https://search.censys.io/api/v1/account', headers=self.headers, auth=auth).json()
            pass
        return httpResponse
        pass

    def count( self, query ):
        httpQuery = '?q=%s&per_page=100' % query

        try:
            httpResponse = requests.get('https://search.censys.io/api/v2/hosts/search' + httpQuery, headers=self.headers, auth=self.auth[0]).json()
            if httpResponse['code'] == 429:
                print(f"The quota has been reached for {Main.textHighlight(self.auth[0][0])}, there is {Main.textHighlight(str(len(self.auth)-1)) + '/' + Main.textHighlight(str(self.totalAuth))} auths left, switching ...")
                del self.auth[0]
                return self.count(query)
                pass
            if httpResponse['code'] == 403:
                del self.auth[0]
                print(f"The credentials for {Main.textHighlight(self.auth[0][0])} are invalid, there is {Main.textHighlight(str(len(self.auth)-1)) + '/' + Main.textHighlight(str(self.totalAuth))} auths left, switching ...")
                return self.count(query)
                pass
            if httpResponse['code'] == 200:
                self.totalCount = int(httpResponse['result']['total'])
                return self.totalCount
                pass
        except:
            time.sleep(1)
            return self.count(query)
            pass 
        pass

    def search( self, query, cursor=False ):
        httpQuery = '?q=%s&per_page=100' % (query) if not cursor else '?q=%s&per_page=100&cursor=%s' % (query, cursor)

        try:
            httpResponse = requests.get('https://search.censys.io/api/v2/hosts/search' + httpQuery, headers=self.headers, auth=self.auth[0]).json()
            if httpResponse['code'] == 429:
                print(f"The quota has been reached for {Main.textHighlight(self.auth[0][0])}, there is {Main.textHighlight(str(len(self.auth)-1)) + '/' + Main.textHighlight(str(self.totalAuth))} auths left, switching ...")
                del self.auth[0]
                pass
            with open(self.outputFile, 'a+') as file:
                for result in httpResponse['result']['hits']:
                    self.rawData += f'{result["ip"]}\n'
                    print(f"{Main.textHighlight(len(self.rawData.splitlines()))} results found ...", end='\r')
                    file.write(f'{result["ip"]}\n')
                    pass
                file.close()
                pass
            if len(self.auth) == 0:
                print(f'No more auths usable, all data have been saved in {Main.textHighlight(self.tempFile)}')
                return False
                pass
            if httpResponse['result']['links']['next'] == '' or len(self.rawData.splitlines()) >= self.totalCount:
                print(f"The scan is {Main.textHighlight('finished')}, all results has been saved in {Main.textHighlight(self.tempFile)}")
                print(f'All data have been saved in {Main.textHighlight(self.tempFile)}')
                pass
            if httpResponse['code'] == 200:
                time.sleep(1)
                self.search(query, httpResponse['result']['links']['next'])
                pass
        except:
            time.sleep(1)
            self.search(query, cursor)
            pass
        pass

def main():
    if not os.path.exists(__EXECDIR__ + 'config.txt'):
        with open(__EXECDIR__ + 'config.txt', 'wb') as file:
            file.write(b'')
            file.close()
            pass
        pass

    if "--config" in sys.argv:
        Setup.config()
        return False
    elif "--help" in sys.argv:
        print(f"""{Main.textHighlight('Usage:')} censys-client '<query>' [--config --help]""")
        sys.exit()
        pass

    if len(sys.argv) < 2:
        print(f"""{Main.textHighlight('Usage:')} censys-client '<query>' [--config --help]""")
        sys.exit()
        pass

    censys = Censys( Setup.getConfig(), None)

    print(f"There is {Main.textHighlight(len(censys.auth))} accounts loaded for {Main.textHighlight(str(censys.quota['used']) + '/' + str(censys.quota['allowance']))} queries usable.")
    print(f"All data are going to be saved in {Main.textHighlight(censys.outputFile)}\n")

    totalCount = censys.count( sys.argv[1] )
    print(f"{Main.textHighlight(totalCount)} results found ...")

    print(f"Searching for {Main.textHighlight(sys.argv[1])} ...")
    censys.search( sys.argv[1] )
    pass
