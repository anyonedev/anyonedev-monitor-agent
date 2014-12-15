
import unittest
from monitor.metrics.log.GCLogger import GCLogLineParser

class GCLogLineParserTest(unittest.TestCase):
    
    parser = GCLogLineParser()
    def test1(self):
        log = "1.580: [Full GC [PSYoungGen: 6962K->0K(153600K)] [ParOldGen: 72K->6710K(349696K)] 7034K->6710K(503296K) [PSPermGen: 14167K->14162K(28672K)], 0.1099306 secs] [Times: user=0.16 sys=0.00, real=0.11 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(1.580, data["timestamp"], msg)
        self.assertEqual("ParallelFullGC", data["type"], msg)
        self.assertEqual(0.1099306, data["response"], msg)
        
        self.assertEqual(6962, data["heap_new-before"], msg)
        self.assertEqual(0, data["heap_new-after"], msg)
        self.assertEqual(153600, data["heap_new-total"], msg)
        
        self.assertEqual(72, data["heap_old-before"], msg)
        self.assertEqual(6710, data["heap_old-after"], msg)
        self.assertEqual(349696, data["heap_old-total"], msg)
        
        self.assertEqual(14167, data["perm-before"], msg)
        self.assertEqual(14162, data["perm-after"], msg)
        self.assertEqual(28672, data["perm-total"], msg)

        self.assertEqual(7034, data["heap_all-before"], msg)
        self.assertEqual(503296, data["heap_all-total"], msg)
        self.assertEqual(6710, data["heap_all-after"], msg)

             
    def test2(self):
        log = "2.380: [GC 2.380: [ParNew: 32768K->4204K(49152K), 0.0128980 secs] 32768K->4204K(114688K), 0.0130090 secs] [Times: user=0.04 sys=0.00, real=0.01 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(2.380, data["timestamp"], msg)
        self.assertEqual("ParNew", data["type"], msg)
        self.assertEqual(0.0130090, data["response"], msg)
        
        self.assertEqual(32768, data["heap_new-before"], msg)
        self.assertEqual(4204, data["heap_new-after"], msg)
        self.assertEqual(49152, data["heap_new-total"], msg)

        self.assertEqual(32768, data["heap_all-before"], msg)
        self.assertEqual(4204, data["heap_all-after"], msg)
        self.assertEqual(114688, data["heap_all-total"], msg)
        
    def test3(self):
        log = "9.815: [GC 9.815: [ParNew: 32768K->10796K(49152K), 0.0286700 secs] 52540K->30568K(114688K) icms_dc=0 , 0.0287550 secs] [Times: user=0.09 sys=0.00, real=0.03 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(9.815, data["timestamp"], msg)
        self.assertEqual("ParNew", data["type"], msg)
        self.assertEqual(0.028755, data["response"], msg)
        
        self.assertEqual(32768, data["heap_new-before"], msg)
        self.assertEqual(10796, data["heap_new-after"], msg)
        self.assertEqual(49152, data["heap_new-total"], msg)

        self.assertEqual(52540, data["heap_all-before"], msg)
        self.assertEqual(30568, data["heap_all-after"], msg)
        self.assertEqual(114688, data["heap_all-total"], msg)    
        
    def test4(self):
        log = "3.072: [GC [1 CMS-initial-mark: 0K(65536K)] 19136K(114688K), 0.0215880 secs] [Times: user=0.04 sys=0.00, real=0.02 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(3.072, data["timestamp"], msg)
        self.assertEqual("CMS-initial-mark", data["type"], msg)
     
    def test5(self):
        log = "3.094: [CMS-concurrent-mark-start]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(3.094, data["timestamp"], msg)
        self.assertEqual("CMS-concurrent-mark-start", data["type"], msg) 
    
    def test6(self):
        log = "3.131: [CMS-concurrent-mark: 0.034/0.037 secs] [Times: user=0.12 sys=0.00, real=0.04 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(3.131, data["timestamp"], msg)
        self.assertEqual("CMS-concurrent-mark", data["type"], msg)
        self.assertEqual(0.037, data["response"], msg)
    
    def test7(self):
        log = "3.132: [CMS-concurrent-preclean-start]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(3.132, data["timestamp"], msg)
        self.assertEqual("CMS-concurrent-preclean-start", data["type"], msg)
        
    def test8(self):
        log = "3.149: [CMS-concurrent-preclean: 0.014/0.018 secs] [Times: user=0.07 sys=0.00, real=0.01 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(3.149, data["timestamp"], msg)
        self.assertEqual("CMS-concurrent-preclean", data["type"], msg)
        self.assertEqual(0.018, data["response"], msg)
    
    def test9(self):
        log = "3.149: [CMS-concurrent-abortable-preclean-start]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(3.149, data["timestamp"], msg)
        self.assertEqual("CMS-concurrent-abortable-preclean-start", data["type"], msg)
         
    def test10(self):
        log = "17.418: [CMS-concurrent-abortable-preclean: 0.353/1.423 secs] [Times: user=4.60 sys=0.07, real=1.42 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(17.418, data["timestamp"], msg)
        self.assertEqual("CMS-concurrent-abortable-preclean", data["type"], msg)
        self.assertEqual(1.423, data["response"], msg)
    
    def test11(self):
        log = "3.242: [Full GC 3.242: [CMS3.243: [CMS-concurrent-abortable-preclean: 0.046/0.093 secs] [Times: user=0.36 sys=0.00, real=0.10 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(3.242, data["timestamp"], msg)
        self.assertEqual("CMS-concurrent-abortable-preclean-fullgc0", data["type"], msg)
        self.assertEqual(0.093, data["response"], msg)
    
    def test12(self):
        log = "63.533: [Full GC (System) 63.533: [CMS63.534: [CMS-concurrent-abortable-preclean: 0.316/1.244 secs] [Times: user=0.32 sys=0.01, real=1.25 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual(63.533, data["timestamp"], msg)
        self.assertTrue(data["system"], msg)
        self.assertEqual("CMS-concurrent-abortable-preclean-fullgc0", data["type"], msg)
        self.assertEqual(1.244, data["response"], msg)

    def test13(self):
        log = "  (concurrent mode failure): 0K->7015K(65536K), 0.1244810 secs] 22902K->7015K(114688K), [CMS Perm : 21242K->21237K(21248K)], 0.1246890 secs] [Times: user=0.19 sys=0.05, real=0.13 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-concurrent-abortable-preclean-fullgc1", data["type"], msg)
        self.assertEqual(0.124689, data["response"], msg)
        
        self.assertEqual(0, data["heap_1-before"], msg)
        self.assertEqual(7015, data["heap_1-after"], msg)
        self.assertEqual(65536, data["heap_1-total"], msg)
        
        self.assertEqual(22902, data["heap_2-before"], msg)
        self.assertEqual(7015, data["heap_2-after"], msg)
        self.assertEqual(114688, data["heap_2-total"], msg)

        self.assertEqual(21242, data["perm-before"], msg)
        self.assertEqual(21237, data["perm-after"], msg)
        self.assertEqual(21248, data["perm-total"], msg) 
    
    def test14(self):
        log = "  (concurrent mode interrupted): 44784K->40478K(65536K), 0.4974690 secs] 66630K->40478K(114688K), [CMS Perm : 77174K->77148K(128736K)], 0.4975800 secs] [Times: user=0.46 sys=0.03, real=0.50 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-concurrent-abortable-preclean-fullgc1", data["type"], msg)
        self.assertEqual(0.49758, data["response"], msg)
        
        self.assertEqual(44784, data["heap_1-before"], msg)
        self.assertEqual(40478, data["heap_1-after"], msg)
        self.assertEqual(65536, data["heap_1-total"], msg)
        
        self.assertEqual(66630, data["heap_2-before"], msg)
        self.assertEqual(40478, data["heap_2-after"], msg)
        self.assertEqual(114688, data["heap_2-total"], msg)

        self.assertEqual(77174, data["perm-before"], msg)
        self.assertEqual(77148, data["perm-after"], msg)
        self.assertEqual(128736, data["perm-total"], msg) 
    
    def test15(self):
        log = " CMS: abort preclean due to time 36.855: [CMS-concurrent-abortable-preclean: 1.280/5.084 secs] [Times: user=1.29 sys=0.00, real=5.09 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-concurrent-abortable-preclean-failure-time", data["type"], msg)
        self.assertEqual(36.855, data["timestamp"], msg)
        self.assertEqual(5.084, data["response"], msg)
     
    def test16(self):
        log = "3.368: [GC [1 CMS-initial-mark: 7015K(65536K)] 7224K(114688K), 0.0004900 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-initial-mark", data["type"], msg)
        self.assertEqual(3.368, data["timestamp"], msg)
    
    def test17(self):
        log = "3.428: [CMS-concurrent-mark: 0.059/0.060 secs] [Times: user=0.22 sys=0.00, real=0.06 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-concurrent-mark", data["type"], msg)
        self.assertEqual(3.428, data["timestamp"], msg)
        self.assertEqual(0.06, data["response"], msg)

    def test18(self):
        log = "3.431: [CMS-concurrent-preclean: 0.002/0.002 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-concurrent-preclean", data["type"], msg)
        self.assertEqual(3.431, data["timestamp"], msg)
        self.assertEqual(0.002, data["response"], msg)
        
    def test19(self):
        log = "3.431: [GC[YG occupancy: 1005 K (49152 K)]3.431: [Rescan (parallel) , 0.0080410 secs]3.439: [weak refs processing, 0.0000100 secs]3.439: [class unloading, 0.0014010 secs]3.441: [scrub symbol & string tables, 0.0032440 secs] [1 CMS-remark: 7015K(65536K)] 8021K(114688K), 0.0130490 secs] [Times: user=0.03 sys=0.00, real=0.02 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-remark", data["type"], msg)
        self.assertEqual(3.431, data["timestamp"], msg)
        self.assertEqual(0.013049, data["response"], msg)
        
    def test20(self):
        log = "3.444: [CMS-concurrent-sweep-start]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-concurrent-sweep-start", data["type"], msg)
        self.assertEqual(3.444, data["timestamp"], msg)
    
    def test21(self):
        log = "3.468: [CMS-concurrent-sweep: 0.024/0.024 secs] [Times: user=0.06 sys=0.00, real=0.02 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-concurrent-sweep", data["type"], msg)
        self.assertEqual(3.468, data["timestamp"], msg)    
        self.assertEqual(0.024, data["response"], msg)
    
    def test22(self):
        log = "3.444: [CMS-concurrent-reset-start]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-concurrent-reset-start", data["type"], msg)
        self.assertEqual(3.444, data["timestamp"], msg)
    
    def test23(self):
        log = "3.468: [CMS-concurrent-reset: 0.000/0.000 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("CMS-concurrent-reset", data["type"], msg)
        self.assertEqual(3.468, data["timestamp"], msg)
        self.assertEqual(0.0, data["response"], msg)    
    
    def test24(self):
        log = "7.992: [Full GC 7.992: [CMS: 6887K->19772K(65536K), 0.4137230 secs] 34678K->19772K(114688K), [CMS Perm : 54004K->53982K(54152K)] icms_dc=0 , 0.4140100 secs] [Times: user=0.68 sys=0.14, real=0.41 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("FullGC", data["type"], msg)
        self.assertEqual(7.992, data["timestamp"], msg)
        self.assertEqual(0.41401, data["response"], msg)
        
        self.assertEqual(34678, data["heap_all-before"], msg)
        self.assertEqual(19772, data["heap_all-after"], msg)
        self.assertEqual(114688, data["heap_all-total"], msg)
        
        self.assertEqual(6887, data["heap_cms-before"], msg)
        self.assertEqual(19772, data["heap_cms-after"], msg)
        self.assertEqual(65536, data["heap_cms-total"], msg)
        
        self.assertEqual(54004, data["perm-before"], msg)
        self.assertEqual(53982, data["perm-after"], msg)
        self.assertEqual(54152, data["perm-total"], msg)

    def test25(self):
        log = "123.533: [Full GC (System) 123.533: [CMS: 39710K->34052K(65536K), 0.4852070 secs] 62832K->34052K(114688K), [CMS Perm : 77479K->76395K(128928K)], 0.4853310 secs] [Times: user=0.47 sys=0.01, real=0.48 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("FullGC", data["type"], msg)
        self.assertTrue(data["system"], msg)
        self.assertEqual(123.533, data["timestamp"], msg)
        self.assertEqual(0.485331, data["response"], msg)
        
        self.assertEqual(62832, data["heap_all-before"], msg)
        self.assertEqual(34052, data["heap_all-after"], msg)
        self.assertEqual(114688, data["heap_all-total"], msg)
        
        self.assertEqual(39710, data["heap_cms-before"], msg)
        self.assertEqual(34052, data["heap_cms-after"], msg)
        self.assertEqual(65536, data["heap_cms-total"], msg)
        
        self.assertEqual(77479, data["perm-before"], msg)
        self.assertEqual(76395, data["perm-after"], msg)
        self.assertEqual(128928, data["perm-total"], msg)
        
    def test26(self):
        log = "162.002: [GC [PSYoungGen: 39323K->3653K(49152K)] 87187K->56999K(114688K), 0.0207580 secs] [Times: user=0.08 sys=0.00, real=0.02 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("ParallelGC", data["type"], msg)
        self.assertEqual(162.002, data["timestamp"], msg)
        self.assertEqual(0.020758, data["response"], msg)
        
        self.assertEqual(87187, data["heap_all-before"], msg)
        self.assertEqual(56999, data["heap_all-after"], msg)
        self.assertEqual(114688, data["heap_all-total"], msg)
        
        self.assertEqual(39323, data["heap_new-before"], msg)
        self.assertEqual(3653, data["heap_new-after"], msg)
        self.assertEqual(49152, data["heap_new-total"], msg)
     
    def test27(self):
        log = "162.657: [Full GC [PSYoungGen: 6189K->0K(50752K)] [PSOldGen: 58712K->43071K(65536K)] 64902K->43071K(116288K) [PSPermGen: 81060K->81060K(81152K)], 0.3032230 secs] [Times: user=0.30 sys=0.00, real=0.30 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("ParallelFullGC", data["type"], msg)
        self.assertEqual(162.657, data["timestamp"], msg)
        self.assertEqual(0.303223, data["response"], msg)
        
        self.assertEqual(58712, data["heap_old-before"], msg)
        self.assertEqual(43071, data["heap_old-after"], msg)
        self.assertEqual(65536, data["heap_old-total"], msg)
        
        self.assertEqual(6189, data["heap_new-before"], msg)
        self.assertEqual(0, data["heap_new-after"], msg)
        self.assertEqual(50752, data["heap_new-total"], msg) 
        
        self.assertEqual(81060, data["perm-before"], msg)
        self.assertEqual(81060, data["perm-after"], msg)
        self.assertEqual(81152, data["perm-total"], msg)
        
        self.assertEqual(64902, data["heap_all-before"], msg)
        self.assertEqual(43071, data["heap_all-after"], msg)
        self.assertEqual(116288, data["heap_all-total"], msg)   

    def test28(self):
        log = "4.687: [GC 4.687: [DefNew: 33343K->649K(49152K), 0.0021450 secs] 45309K->12616K(114688K), 0.0021800 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("SerialGC", data["type"], msg)
        self.assertEqual(4.687, data["timestamp"], msg)
        self.assertEqual(0.00218, data["response"], msg)
        
        self.assertEqual(33343, data["heap_new-before"], msg)
        self.assertEqual(649, data["heap_new-after"], msg)
        self.assertEqual(49152, data["heap_new-total"], msg) 
        
        self.assertEqual(45309, data["heap_all-before"], msg)
        self.assertEqual(12616, data["heap_all-after"], msg)
        self.assertEqual(114688, data["heap_all-total"], msg) 
    
    def test29(self):
        log = "4.899: [Full GC 4.899: [Tenured: 11966K->12899K(65536K), 0.1237750 secs] 22655K->12899K(114688K), [Perm : 32122K->32122K(32128K)], 0.1238590 secs] [Times: user=0.11 sys=0.00, real=0.13 secs]"
        data = self.parser.parse(log)
        msg = "解析不正确"
        self.assertNotEqual(data, None, msg)
        self.assertEqual("SerialFullGC", data["type"], msg)
        self.assertEqual(4.899, data["timestamp"], msg)
        self.assertEqual(0.123859, data["response"], msg)
        
        self.assertEqual(11966, data["heap_old-before"], msg)
        self.assertEqual(12899, data["heap_old-after"], msg)
        self.assertEqual(65536, data["heap_old-total"], msg) 
        
        self.assertEqual(22655, data["heap_all-before"], msg)
        self.assertEqual(12899, data["heap_all-after"], msg)
        self.assertEqual(114688, data["heap_all-total"], msg) 
        
        self.assertEqual(32122, data["perm-before"], msg)
        self.assertEqual(32122, data["perm-after"], msg)
        self.assertEqual(32128, data["perm-total"], msg) 
        
if __name__ == "__main__":
    unittest.main()
