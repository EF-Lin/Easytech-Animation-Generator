from dataclasses import dataclass
import os
from error import SizeError


@dataclass
class Bin:
    """
    Limit: 4bits.
    Usage: generate_ani -> generate_bin -> generate_xml.
    Known error types: SizeError, AttributeError, IndexError.
    """
    FRAME: int
    NUM: int
    TIME: int = 4
    DEFAULT_PATH: str = '.'

    def __post_init__(self) -> str or bool:
        self.ani_name = []
        self.pic_name = []
        self.string_index = []
        self.file_name = f'{self.NUM}x{self.FRAME}frame_animation'
        self.file_type = ['.bin', '.xml']
        self.main_path = os.path.normpath(self.DEFAULT_PATH)
        self.bin_path = os.path.normpath(f'{self.DEFAULT_PATH}/{self.file_name}{self.file_type[0]}')
        self.xml_path = os.path.normpath(f'{self.DEFAULT_PATH}/{self.file_name}{self.file_type[1]}')

    def __str__(self):
        return 'Easytech animation generator developed by EF'

    @staticmethod
    def int_to_2bit_hex(n: int) -> str:
        n = str(hex(n)).replace('0x', '').upper()
        if len(n) == 1:
            return '0' + n
        elif len(n) == 2:
            return n
        else:
            raise SizeError

    @staticmethod
    def int_to_4bit_hex(n: int) -> list:
        n = str(hex(n)).replace('0x', '').upper()
        while len(n) <= 4:
            if len(n) == 4:
                return [n[2:4], n[0:2]]
            else:
                n = '0' + n
        else:
            raise SizeError

    @staticmethod
    def int_to_8bit_hex(n: int) -> list:
        n = str(hex(n)).replace('0x', '').upper()
        while len(n) <= 8:
            if len(n) == 8:
                return [n[6:8], n[4:6], n[2:4], n[0:2]]
            else:
                n = '0' + n
        else:
            raise SizeError

    @staticmethod
    def list_to_byte(data: list) -> bytes:
        return bytes.fromhex(''.join(data[0:len(data)]))

    def size_calculator_8bit(self, header_size: int, repeater_size: int = 0, n: int = 0) -> [list, int]:
        return self.int_to_8bit_hex(repeater_size * n + header_size), repeater_size * n + header_size

    def init_element(self):
        # element info
        element_num = self.NUM * (self.FRAME + 1)
        element_size_list, self.element_size = self.size_calculator_8bit(0x10, 0x2c, element_num)
        # 0x10
        element_header = ['42', '45', '4C', '45', 'xx', 'xx', 'xx', 'xx',
                          '21', '00', '00', '00', '38', '74', '5E', '00']
        element_header[4:8] = element_size_list
        # 0x2c
        # repeat self.element_num
        element_repeater = ['00', '00', '80', '3F', '00', '00', '00', '00',
                            '00', '00', '00', '00', '00', '00', '80', '3F',
                            '8D', '97', 'A3', 'C1', '17', '19', '83', 'C2',
                            '00', '00', '80', '3F', '00', '00', '00', '00',
                            '00', '00', '00', '00', '10', '02', '00', '00',
                            '00', '00', '5E', '00']
        for i in range(element_num):
            element_header.extend(element_repeater)
        self.element_byte = self.list_to_byte(element_header)

    def init_index(self):
        index_num = self.NUM * self.FRAME * 2
        index_size_list, self.index_size = self.size_calculator_8bit(0x10, 0x8, index_num)
        # 0x10
        index_header = ['42', '58', '44', '49', 'xx', 'xx', 'xx', 'xx',
                        '3C', '00', '00', '00', '88', 'E9', '86', '00']
        index_header[4:8] = index_size_list
        # 0x8
        index_repeater = self.generate_index_repeater()
        index_header.extend(index_repeater)
        self.index_byte = self.list_to_byte(index_header)

    def generate_index_repeater(self) -> list:
        index = []
        i = 0
        for _ in range(self.NUM):
            for j in range(self.FRAME * 2):
                if j < self.FRAME:
                    n1 = self.int_to_2bit_hex(i)
                    n2 = self.int_to_2bit_hex(i + 1)
                    index_ani = [n1, '00', '00', '00', n2, '00', '00', '00']
                    index.extend(index_ani)
                    i += 1
                else:
                    n = self.int_to_2bit_hex(i)
                    index_pic = [n, '00', '00', '00', 'FF', 'FF', 'FF', 'FF']
                    index.extend(index_pic)
                    i += 1 if j == self.FRAME * 2 - 1 else 0
        return index

    def init_frame(self):
        frame_num = self.NUM * self.FRAME * 2
        frame_size_list, self.frame_size = self.size_calculator_8bit(0x10, 0x8, frame_num)
        # 0x10
        frame_header = ['42', '4D', '52', '46', 'xx', 'xx', 'xx', 'xx',
                        '3C', '00', '00', '00', '70', 'E7', '86', '00']
        frame_header[4:8] = frame_size_list
        # 0x8
        frame_repeater = self.generate_frame_repeater()
        frame_header.extend(frame_repeater)
        self.frame_byte = self.list_to_byte(frame_header)

    def generate_frame_repeater(self) -> list:
        frame = []
        i = 0
        for _ in range(self.NUM):
            for j in range(self.FRAME * 2):
                if j < self.FRAME:
                    n = self.int_to_2bit_hex(i)
                    frame.append(n)
                    i += self.TIME
                else:
                    i = 0
                    frame.append('00')
                frame.extend(['00', '01', '00', '68', '00', '08', '00'])
        return frame

    def init_layer(self):
        layer_num = self.NUM * (self.FRAME + 1)
        layer_size_list, self.layer_size = self.size_calculator_8bit(0x10, 0x8, layer_num)
        # 0x10
        layer_header = ['42', '59', '41', '4C', 'xx', 'xx', 'xx', 'xx',
                        '21', '00', '00', '00', '00', 'DA', '86', '00']
        layer_header[4:8] = layer_size_list
        # 0x8
        # repeat self.NUM
        layer_repeater = self.generate_layer_repeater()
        for i in range(self.NUM):
            layer_header.extend(layer_repeater)
        self.layer_byte = self.list_to_byte(layer_header)

    def generate_layer_repeater(self) -> list:
        layer = [self.int_to_2bit_hex(self.FRAME), '00', '00', '00', 'B1', '14', '15', '77']
        for i in range(self.FRAME):
            layer.extend(['01', '00', '00', '00', 'B1', '14', '15', '77'])
        return layer

    def init_string(self):
        string_name_byte = self.generate_string()
        string_size_list, self.string_size = self.size_calculator_8bit(0xc + len(string_name_byte))
        # 0xc
        string_header = ['42', '52', '54', '53', '00', '00', '00', '00', '00', '00', '00', '00']
        string_header[4:8] = string_size_list
        self.string_byte = self.list_to_byte(string_header) + string_name_byte

    def generate_string(self) -> bytes:
        string = b''
        i = 0
        for j in range(1, self.NUM + 1):
            name = f'動畫{j}By EF,TW'
            self.ani_name.append(name)
            string += name.encode('utf-8')
            string += b'\x00'
            self.string_index.append(i)
            i = len(string)
            for k in range(self.FRAME):
                # name = f'動畫{j}第{k}幀'
                name = f'{j}{k}'
                self.pic_name.append(name)
                string += name.encode('utf-8')
                string += b'\x00'
                self.string_index.append(i)
                i = len(string)
        return string

    def init_item(self):
        item_num = self.NUM * (self.FRAME + 1)
        item_size_list, self.item_size = self.size_calculator_8bit(0x10, 0x38, item_num)
        # 0x10
        item_header = ['42', '4D', '54', '49', 'xx', 'xx', 'xx', 'xx',
                       '21', '00', '00', '00', '78', '84', '83', '00']
        item_header[4:8] = item_size_list
        # 0x38
        item_repeater = self.generate_item_repeater()
        item_header.extend(item_repeater)
        self.item_byte = self.list_to_byte(item_header)

    def generate_item_repeater(self) -> list:
        items = []
        i = 0
        for j in range(self.NUM):
            item = ['xx', '00', '00', '00', 'xx', 'xx', '00', '00',
                    '00', '00', '00', '00', '00', '00', '00', '00',
                    '00', '00', '00', '00', '00', '00', '00', '00',
                    # info
                    '00', '00', '00', '00', 'xx', 'xx', '00', '00',
                    '01', '00', '00', '00', 'xx', 'xx', '00', '00',
                    'xx', 'xx', '00', '00', '48', '04', '00', '00',
                    'D0', 'F6', '74', '00', '0F', 'F7', '0F', '77']
            item[0] = self.int_to_2bit_hex(i)
            item[4:6] = self.int_to_4bit_hex(self.string_index[i])
            item[28:30] = self.int_to_4bit_hex(self.TIME * self.FRAME)
            item[36:38] = item[40:42] = self.int_to_4bit_hex(self.FRAME)
            items.extend(item)
            i += 1
            for k in range(self.FRAME):
                item = ['xx', '00', '00', '00', 'xx', 'xx', '00', '00',
                        '00', '00', '00', '00', '00', '00', '00', '00',
                        '00', '00', '00', '00', '00', '00', '00', '00',
                        # info
                        '01', '00', '00', '00', '01', '00', '00', '00',
                        '01', '00', '00', '00', '01', '00', '00', '00',
                        '01', '00', '00', '00', '48', '04', '00', '00',
                        'D0', 'F6', '74', '00', '0F', 'F7', '0F', '77']
                item[0] = self.int_to_2bit_hex(i)
                item[4:6] = self.int_to_4bit_hex(self.string_index[i])
                items.extend(item)
                i += 1
        return items

    def init_header(self):
        # 0x14
        header = ['42', '49', '4C', '45', '03', '00', '00', '00',
                  'xx', 'xx', 'xx', 'xx', '14', '00', '06', '00',
                  '00', '00', 'C0', '41']
        header[8:12] = self.int_to_8bit_hex(self.element_size + self.index_size + self.frame_size
                                            + self.layer_size + self.item_size + self.string_size + 0x14)
        self.header_byte = self.list_to_byte(header)

    def generate_ani(self) -> bool:
        self.init_element()
        self.init_index()
        self.init_frame()
        self.init_layer()
        self.init_string()
        self.init_item()
        self.init_header()
        return True

    def generate_bin(self) -> bool:
        with open(self.bin_path, 'wb') as f:
            f.write(self.header_byte + self.element_byte + self.index_byte + self.frame_byte + self.layer_byte
                    + self.item_byte + self.string_byte)
        return True

    def generate_xml(self) -> bool:
        xml = f'<Texture name="{self.file_name}.png" />\n<Images>'
        k = 0
        for i in self.ani_name:
            xml += f'\n\t<!--animation name: {i}-->'
            for j in self.pic_name[k:k+self.FRAME]:
                xml += f'\n\t<Image name="{j}.png" x="0" y="0" w="0" h="0" refx="0" refy="0" />'
            k += self.FRAME
        xml += '\n</Images>\n<!--made by EF-->'
        with open(self.xml_path, 'w+') as f:
            f.write(xml)
        return True


if __name__ == '__main__':
    a = Bin(NUM=3, FRAME=10)
    a.generate_ani()
    print(a.generate_bin())
    print(a.generate_xml())
