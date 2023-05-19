import os
import sys
import unittest


class InstallationTests(unittest.TestCase): 

    def test_auralobster_install_1(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} auralobster install")
    
    def test_auralobster_install_2(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} install auralobster")
    
    def test_ingtepreter_install_1(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} ingtepreter install")
    
    def test_ingtepreter_install_2(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} install ingtepreter")


# unittest를 실행
if __name__ == '__main__':  
    unittest.main()
