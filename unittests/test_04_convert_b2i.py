import os
import sys
import unittest


class ConvertBfToIngTests(unittest.TestCase): 

    def test_ingchicken_convert_b2i_1(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} "
            "ingchicken convert b2i helloworld.bf samples/helloworld.ingc")
    
    def test_ingchicken_convert_b2i_2(self):
        unittest_path = os.path.dirname(os.path.abspath(__file__))
        package_path = os.path.dirname(unittest_path)
        
        if package_path not in sys.path:
            sys.path = [package_path] + sys.path
        print(sys.path)
        
        os.system(f"python {os.path.join(package_path, 'runner.py')} "
            "ingchicken convert b2i helloing.bf samples/helloing.ingc")


# unittest를 실행
if __name__ == '__main__':  
    unittest.main()
