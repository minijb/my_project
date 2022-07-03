import argparse

def main():
    parser = argparse.ArgumentParser(description='''
                                     
    ''')
    parser.add_argument('--foo',help='foo help')
    args = parser.parse_args()
    
if __name__=='__main__':
    main()