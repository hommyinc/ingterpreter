import os
import sys
import unittest


class UninstallationTests(unittest.TestCase): 

    def test_auralobster_uninstall_1(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} auralobster uninstall")
    
    def test_auralobster_uninstall_2(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} uninstall auralobster")
    
    def test_ingtepreter_uninstall_1(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} ingtepreter uninstall")
    
    def test_ingtepreter_uninstall_2(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} uninstall ingtepreter")


# unittest를 실행
if __name__ == '__main__':  
    unittest.main()
