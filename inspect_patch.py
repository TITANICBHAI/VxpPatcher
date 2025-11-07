import struct

def inspect_vxp(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"\n{'='*60}")
    print(f"Inspecting: {filename}")
    print(f"{'='*60}")
    
    # Check ELF header
    if data[:4] != b'\x7fELF':
        print("ERROR: Not a valid ELF file!")
        return
    
    print("✓ Valid ELF file")
    
    # Parse ELF header
    e_shoff = struct.unpack('<I', data[0x20:0x24])[0]
    e_shentsize = struct.unpack('<H', data[0x2E:0x30])[0]
    e_shnum = struct.unpack('<H', data[0x30:0x32])[0]
    metadata_start = e_shoff + (e_shnum * e_shentsize)
    
    print(f"\nELF Header Information:")
    print(f"  Section header offset: {e_shoff}")
    print(f"  Section header size: {e_shentsize}")
    print(f"  Number of sections: {e_shnum}")
    print(f"  Metadata starts at: {metadata_start}")
    
    # Parse metadata tags
    print(f"\nMetadata Tags:")
    offset = metadata_start
    tag_num = 0
    
    while offset < len(data):
        tag_id = data[offset]
        
        if tag_id == 0xFF:
            print(f"\n  Tag #{tag_num}: END (0xFF)")
            print(f"    Offset: {offset}")
            break
        
        if offset + 3 > len(data):
            print(f"\n  ERROR: Truncated tag at offset {offset}")
            break
        
        tag_length = struct.unpack('<H', data[offset+1:offset+3])[0]
        tag_data = data[offset+3:offset+3+tag_length]
        
        print(f"\n  Tag #{tag_num}:")
        print(f"    Tag ID: 0x{tag_id:02X}", end="")
        
        if tag_id == 0x01:
            print(" (IMSI)")
            imsi = tag_data.decode('ascii', errors='replace').rstrip('\x00')
            print(f"    IMSI Value: {imsi}")
            if imsi.startswith('9'):
                print(f"    → User IMSI: {imsi[1:]}")
        else:
            print()
        
        print(f"    Offset: {offset}")
        print(f"    Length: {tag_length} bytes")
        print(f"    Raw data: {tag_data[:20]}{'...' if len(tag_data) > 20 else ''}")
        print(f"    Hex: {tag_data.hex()[:40]}{'...' if len(tag_data.hex()) > 40 else ''}")
        
        offset += 3 + tag_length
        tag_num += 1
    
    print(f"\nFile size: {len(data)} bytes")
    print(f"Metadata size: {len(data) - metadata_start} bytes")

# Inspect both files
inspect_vxp('test_original.vxp')
inspect_vxp('test_patched.vxp')

# Show binary comparison
print(f"\n{'='*60}")
print("Binary Comparison")
print(f"{'='*60}")

with open('test_original.vxp', 'rb') as f:
    original = f.read()
with open('test_patched.vxp', 'rb') as f:
    patched = f.read()

print(f"\nOriginal size: {len(original)} bytes")
print(f"Patched size: {len(patched)} bytes")
print(f"Size difference: +{len(patched) - len(original)} bytes")

# Find metadata start
e_shoff = struct.unpack('<I', original[0x20:0x24])[0]
e_shentsize = struct.unpack('<H', original[0x2E:0x30])[0]
e_shnum = struct.unpack('<H', original[0x30:0x32])[0]
metadata_start = e_shoff + (e_shnum * e_shentsize)

print(f"\nELF headers: {'IDENTICAL' if original[:metadata_start] == patched[:metadata_start] else 'DIFFERENT'}")
print(f"\nMetadata section changes:")
print(f"  Original metadata: {original[metadata_start:].hex()}")
print(f"  Patched metadata:  {patched[metadata_start:].hex()}")
