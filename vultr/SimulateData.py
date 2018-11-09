# simulate test score
from vultr.Node import Node
from vultr.Result import Result

vultrSimulateScore = {
    Node('Frankfurt, DE', 'www.baidu.com'):                 Result({"package": [64, 55, 9, 14], "delay": [262, 369, 342]}, {"package": [65, 64, 1], "delay": [1, 460, 358, 409]},[10,20]),
    Node('Paris, France', 'www.baidu.com'):                 Result({"package": [64, 55, 9, 14], "delay": [261, 459, 372]}, {"package": [69, 64, 5], "delay": [7, 460, 359, 421]},[10,20]),
    Node('Amsterdam,NL', 'www.baidu.com'):                  Result({"package": [64, 62, 2, 3], "delay": [276, 376, 359]},  {"package": [74, 64, 10], "delay": [13, 374, 320, 367]},[10,20]),
    Node('London, UK', 'www.baidu.com'):                    Result({"package": [64, 63, 1, 1], "delay": [310, 469, 430]},  {"package": [72, 64, 8], "delay": [11, 437, 327, 382]},[10,20]),
    Node('Singapore', 'www.baidu.com'):                     Result({"package": [64, 59, 5, 7], "delay": [189, 234, 205]},  {"package": [70, 64, 6], "delay": [8, 223, 186, 205]},[10,20]),
    Node('New York (NJ)', 'www.baidu.com'):                 Result({"package": [64, 64, 0, 0], "delay": [224, 323, 233]},  {"package": [66, 64, 2], "delay": [3, 322, 246, 304]},[10,20]),
    Node('Chicago, Illinois', 'www.baidu.com'):             Result( {"package": [64, 64, 0, 0], "delay": [222, 225, 222]}, {"package": [64, 64, 0], "delay": [0, 320, 222, 290]},[10,20]),
    Node('Tokyo, Japan', 'www.baidu.com'):                  Result({"package": [64, 58, 6, 9], "delay": [155, 208, 179]},  {"package": [134, 60, 74], "delay": [55, 181, 168, 176]},[10,20]),
    Node('Atlanta, Georgia', 'www.baidu.com'):              Result( {"package": [64, 64, 0, 0], "delay": [236, 344, 249]}, {"package": [67, 64, 3], "delay": [4, 382, 277, 342]},[10,20]),
    Node('Miami, Florida', 'www.baidu.com'):                Result({"package": [64, 58, 6, 9], "delay": [269, 309, 289]},  {"package": [67, 64, 3], "delay": [4, 376, 276, 340]},[10,20]),
    Node('Seattle, Washington', 'www.baidu.com'):           Result( {"package": [64, 64, 0, 0], "delay": [173, 229, 208]}, {"package": [64, 64, 0], "delay": [0, 206, 201, 202]},[10,20]),
    Node('Dallas, Texas', 'www.baidu.com'):                 Result({"package": [64, 61, 3, 4], "delay": [224, 289, 269]},  {"package": [67, 64, 3], "delay": [4, 274, 266, 271]},[10,20]),
    Node('Silicon Valley, California', 'www.baidu.com'):    Result( {"package": [64, 63, 1, 1], "delay": [176, 299, 209]}, {"package": [72, 64, 8], "delay": [11, 298, 208, 270]},[10,20]),
    Node('Los Angeles, California', 'www.baidu.com'):       Result( {"package": [64, 59, 5, 7], "delay": [188, 234, 218]}, {"package": [73, 64, 9], "delay": [12, 216, 210, 214]},[10,20]),
    Node('Sydney, Australia', 'www.baidu.com'):             Result( {"package": [64, 62, 2, 3], "delay": [279, 333, 303]}, {"package": [64, 64, 0], "delay": [0, 311, 296, 304]},[10,20]),
}