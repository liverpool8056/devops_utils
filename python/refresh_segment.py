from NetworkManagement.Models.segment import Segment
from NetworkManagement.Service.SegmentService import SegmentService

if __name__ == '__main__':
    segment_desc_json = '/home/data/tmp/python_script/txt/segment_desc.json'
    segService = SegmentService()
    segment_list = segService.load_from_file(segment_desc_json)
    print(segment_list)
    for segment in segment_list:
        seg = Segment(**segment)
        segService.save(seg)
        print(seg.items())
    seg_list = segService.getAllSegment()
    for seg in seg_list:
        print(seg.items())
