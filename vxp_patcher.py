import struct

class VXPPatcher:
    TAG_IMSI = 0x01
    TAG_END = 0xFF
    
    def __init__(self, vxp_data):
        self.data = bytearray(vxp_data)
        
    def find_metadata_start(self):
        if self.data[:4] != b'\x7fELF':
            raise ValueError("Not a valid ELF/VXP file")
        
        e_shoff = struct.unpack('<I', self.data[0x20:0x24])[0]
        e_shnum = struct.unpack('<H', self.data[0x2E:0x30])[0]
        e_shentsize = struct.unpack('<H', self.data[0x2C:0x2E])[0]
        
        metadata_start = e_shoff + (e_shnum * e_shentsize)
        
        return metadata_start
    
    def parse_tags(self, start_offset):
        tags = []
        offset = start_offset
        
        while offset < len(self.data):
            tag_id = self.data[offset]
            
            if tag_id == self.TAG_END:
                break
                
            if offset + 3 > len(self.data):
                break
                
            tag_length = struct.unpack('<H', self.data[offset+1:offset+3])[0]
            tag_data = self.data[offset+3:offset+3+tag_length]
            
            tags.append({
                'id': tag_id,
                'length': tag_length,
                'data': tag_data,
                'offset': offset
            })
            
            offset += 3 + tag_length
        
        return tags, offset
    
    def patch_imsi(self, imsi_number):
        if not imsi_number.isdigit() or len(imsi_number) != 15:
            raise ValueError("IMSI must be exactly 15 digits")
        
        imsi_tag_value = '9' + imsi_number
        imsi_bytes = imsi_tag_value.encode('ascii') + b'\x00'
        
        metadata_start = self.find_metadata_start()
        tags, tags_end = self.parse_tags(metadata_start)
        
        imsi_tag_idx = None
        for i, tag in enumerate(tags):
            if tag['id'] == self.TAG_IMSI:
                imsi_tag_idx = i
                break
        
        if imsi_tag_idx is not None:
            old_tag = tags[imsi_tag_idx]
            tag_total_size = 3 + old_tag['length']
            del self.data[old_tag['offset']:old_tag['offset']+tag_total_size]
            insert_pos = old_tag['offset']
        else:
            insert_pos = metadata_start
        
        new_tag = bytearray()
        new_tag.append(self.TAG_IMSI)
        new_tag.extend(struct.pack('<H', len(imsi_bytes)))
        new_tag.extend(imsi_bytes)
        
        self.data[insert_pos:insert_pos] = new_tag
        
        return True
    
    def get_patched_data(self):
        return bytes(self.data)
