import struct
from vxp_patcher import VXPPatcher

def create_minimal_vxp():
    """Create a minimal ELF file structure for testing"""
    elf_header = bytearray(52)
    
    # ELF magic number
    elf_header[0:4] = b'\x7fELF'
    
    # ELF class (32-bit)
    elf_header[4] = 1
    
    # Endianness (little-endian)
    elf_header[5] = 1
    
    # ELF version
    elf_header[6] = 1
    
    # e_type (executable)
    struct.pack_into('<H', elf_header, 0x10, 2)
    
    # e_machine (ARM)
    struct.pack_into('<H', elf_header, 0x12, 40)
    
    # e_version
    struct.pack_into('<I', elf_header, 0x14, 1)
    
    # e_shoff - section header offset (we'll put it at byte 100)
    section_header_offset = 100
    struct.pack_into('<I', elf_header, 0x20, section_header_offset)
    
    # e_shentsize - section header entry size (40 bytes is typical for 32-bit ELF)
    section_header_size = 40
    struct.pack_into('<H', elf_header, 0x2E, section_header_size)
    
    # e_shnum - number of section headers (let's say 3)
    num_sections = 3
    struct.pack_into('<H', elf_header, 0x30, num_sections)
    
    # Create a full file with section headers
    vxp_data = bytearray(elf_header)
    
    # Pad to section header offset
    while len(vxp_data) < section_header_offset:
        vxp_data.append(0)
    
    # Add section headers (3 sections × 40 bytes = 120 bytes)
    for i in range(num_sections):
        section_header = bytearray(section_header_size)
        vxp_data.extend(section_header)
    
    # Now metadata should start after the section headers
    # At offset: section_header_offset + (num_sections * section_header_size)
    # = 100 + (3 * 40) = 220
    
    # Add an existing tag (just to test replacement)
    # TAG_NAME = 0x02, length = 5, data = "test\0"
    vxp_data.append(0x02)  # tag ID
    vxp_data.extend(struct.pack('<H', 5))  # length
    vxp_data.extend(b'test\x00')  # data
    
    # End tag
    vxp_data.append(0xFF)
    
    return bytes(vxp_data)

def test_vxp_patcher():
    print("=== VXP Patcher Test ===\n")
    
    # Create a minimal VXP file
    print("1. Creating minimal test VXP file...")
    original_vxp = create_minimal_vxp()
    print(f"   Original file size: {len(original_vxp)} bytes")
    
    # Save original for inspection
    with open('test_original.vxp', 'wb') as f:
        f.write(original_vxp)
    print("   Saved as: test_original.vxp")
    
    # Test IMSI to patch
    test_imsi = "310260123456789"
    print(f"\n2. Patching with IMSI: {test_imsi}")
    
    # Patch the file
    try:
        patcher = VXPPatcher(original_vxp)
        patcher.patch_imsi(test_imsi)
        patched_vxp = patcher.get_patched_data()
        
        print(f"   Patched file size: {len(patched_vxp)} bytes")
        
        # Save patched file
        with open('test_patched.vxp', 'wb') as f:
            f.write(patched_vxp)
        print("   Saved as: test_patched.vxp")
        
        # Verify the patch
        print("\n3. Verifying patch...")
        
        # Calculate where metadata starts
        e_shoff = struct.unpack('<I', patched_vxp[0x20:0x24])[0]
        e_shentsize = struct.unpack('<H', patched_vxp[0x2E:0x30])[0]
        e_shnum = struct.unpack('<H', patched_vxp[0x30:0x32])[0]
        metadata_start = e_shoff + (e_shnum * e_shentsize)
        
        print(f"   ELF header info:")
        print(f"   - e_shoff: {e_shoff}")
        print(f"   - e_shentsize: {e_shentsize}")
        print(f"   - e_shnum: {e_shnum}")
        print(f"   - Metadata starts at: {metadata_start}")
        
        # Parse tags from patched file
        offset = metadata_start
        found_imsi = False
        
        print("\n   Metadata tags found:")
        while offset < len(patched_vxp):
            tag_id = patched_vxp[offset]
            
            if tag_id == 0xFF:
                print(f"   - Tag 0xFF (END) at offset {offset}")
                break
            
            if offset + 3 > len(patched_vxp):
                break
            
            tag_length = struct.unpack('<H', patched_vxp[offset+1:offset+3])[0]
            tag_data = patched_vxp[offset+3:offset+3+tag_length]
            
            if tag_id == 0x01:  # IMSI tag
                found_imsi = True
                imsi_value = tag_data.decode('ascii').rstrip('\x00')
                print(f"   - Tag 0x01 (IMSI) at offset {offset}")
                print(f"     Length: {tag_length} bytes")
                print(f"     Data: {repr(tag_data)}")
                print(f"     IMSI value: {imsi_value}")
                
                # Verify the IMSI
                expected_imsi = '9' + test_imsi
                if imsi_value == expected_imsi:
                    print(f"     ✓ IMSI correctly patched! (Expected: {expected_imsi})")
                else:
                    print(f"     ✗ IMSI mismatch! (Expected: {expected_imsi}, Got: {imsi_value})")
            else:
                print(f"   - Tag 0x{tag_id:02X} at offset {offset}, length {tag_length}")
            
            offset += 3 + tag_length
        
        if found_imsi:
            print("\n✓ SUCCESS: VXP file correctly patched with IMSI!")
        else:
            print("\n✗ FAILURE: IMSI tag not found in patched file!")
        
        return found_imsi
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_vxp_patcher()
    exit(0 if success else 1)
