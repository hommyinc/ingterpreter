import os
import sys
import unittest


class ConvertIngToBfTests(unittest.TestCase): 

    def test_auralobster_convert_i2b(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} "
            "auralobster convert i2b samples/helloworld.auralob helloworld.bf")


# unittest를 실행
if __name__ == '__main__':  
    unittest.main()
