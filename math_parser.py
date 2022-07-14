from numpy import mat
from sympy import Eq
from underthesea import word_tokenize, sent_tokenize
from angle import Angle
from cobj import Cobj
from nlp import text_preprocess
import regex as re
from program import Program
from relation import Relation
from line import Line

class MathParser:

    def __init__(self, hypo: str, question: str):
        self.hypo = hypo
        self.question = question
        self.program = Program()
        self.context = ""
        self.goal_type = 0

    def solve(self):
        self.parse_hypo()
        self.parse_question()
        self.program.solve()
        return self.program.answers

    def parse_hypo(self):

        h_sents = sent_tokenize(self.hypo)
        for sent in h_sents:
            sent = text_preprocess(sent)
            self.parse_triangle(sent)
            self.parse_triangle_equal(sent)
            self.parse_angles(sent)
            self.parse_bisector_1(sent)
            self.parse_bisector_2(sent)
            self.parse_tri_point(sent)
            self.parse_ray(sent)
            self.parse_height(sent)
            self.parse_bisector_out(sent)
            self.parse_edge_eq(sent)

    def parse_question(self):
        q_sents = sent_tokenize(self.question)
        for sent in q_sents:
            sent = text_preprocess(sent)
            self.parse_goal(sent)
            self.parse_angle_q(sent)
            self.parse_relation_1(sent)
            self.parse_relation_2(sent)
            self.parse_relation_3(sent)
            

    def parse_triangle(self, sent: str) -> bool:
        #reg = re.compile(r'tam giác\s+\w*\s*([A-Z]{3})')
        reg = re.compile(r'tam giác \w*\s*([A-Z]{3})\s*(và ([A-Z]{3}))?')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        for match in matches:
            tri_name = match[0]
            self.program.set_triangle(tri_name)
            self.context = tri_name
            if len(match) == 3:
                 tri_name = match[2]
                 self.program.set_triangle(tri_name)
        return True

    def parse_triangle_equal(self, sent: str) -> bool:
        reg = re.compile(r'tam giác ([A-Z]{3}) = tam giác ([A-Z]{3})')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        for match in matches:
            tri1 = match[0]
            tri2 = match[1]
            self.program.set_triangle_equal(tri1, tri2)
            self.context = tri1
        return True

    def parse_angle_1(self, sent: str) -> bool:

        reg = re.compile(r'(^|[^\-\+]\s)[gG]óc\s+([A-Z]{1,3})\s*=\s*(\d{1,3})\b')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        for angle in matches:
            angle_name = angle[1].upper()
            angle_value = angle[2]
            self.program.set_angle(angle_name, angle_value)

        return True

    def parse_angle_2(self, sent: str) -> bool:

        reg = re.compile(r'góc\s([A-Z]{1,3})\s=\sgóc\s([A-Z]{1,3})\s=\s(\d{1,3})')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        
        match = matches[0]
        angle1 = match[0].upper()
        angle2 = match[1].upper()
        angle_value = match[2].upper()
        self.program.set_angle(angle1, angle_value)
        self.program.set_angle(angle2, angle_value)

        return True

    def parse_angle_3(self, sent: str) -> bool:
        if self.context is None: # if not meet triangle yet
            return False

        reg = re.compile(r'[Gg]óc ([A-Z]{1,3}) ([\+\-\*\/]) góc ([A-Z]{1,3}) = (\d{1,3})')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False

        match = matches[0]

        angle1 = match[0]
        op = match[1]
        angle2 = match[2]
        value = int(match[3])

        tri = Cobj.get_triangle(self.context)
        if op == "-":
            eq = Eq(tri.angles[angle1].symb - tri.angles[angle2].symb, value)
        if op == "+":
            eq = Eq(tri.angles[angle1].symb + tri.angles[angle2].symb, value)

        self.program.set_equation(eq)

        return True

    def parse_angle_4(self, sent: str) -> bool:

        reg = re.compile(r'vuông tại ([A-Z]{1})')
        match = reg.search(sent)
        if match is None:
            return False
        
        angle = match.group(1)
        self.program.set_angle(angle, 90)

        return True

    def parse_angles(self, sent: str) -> bool:
        self.parse_angle_1(sent)
        self.parse_angle_2(sent)
        self.parse_angle_3(sent)
        self.parse_angle_4(sent)

    def parse_bisector_1(self, sent: str) -> bool:
        if self.context is None: # if not meet triangle yet
            return False

        reg = re.compile(r'phân giác.+góc\s+([A-Z]{1,3})\s+cắt\s+([A-Z]{2})\s+ở\s+([A-Z]{1})')
        match = reg.search(sent)
        if match is None:
            return False
        from_v = match.group(1).upper()
        to_v = match.group(3).upper()
        self.program.set_bisector_in(self.context, from_v, to_v)

        return True

    def parse_bisector_2(self, sent: str) -> bool:
        if self.context is None: # if not meet triangle yet
            return False

        reg = re.compile(r'phân giác.+góc ([A-Z]{1,3}) và ([A-Z]{1,3}) cắt nhau ở ([A-Z]{1})')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        match = matches[0]
        from_v1 = match[0]
        from_v2 = match[1]
        bi_center = match[2]
        self.program.set_bisector_in(self.context, from_v1)
        self.program.set_bisector_in(self.context, from_v2)
        self.program.set_bisector_center(self.context, bi_center)

        return True

    def parse_bisector_out(self, sent: str) -> bool:
        if self.context is None: # if not meet triangle yet
            return False

        reg = re.compile(r'([A-Z][a-z]).*phân giác.*góc ngoài')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        for match in matches:
            ray_name = match
            self.program.set_bisector_out(self.context, ray_name[0].upper(), ray_name[1])

        return True

    def parse_height(self, sent: str) -> bool:
        if self.context is None: # if not meet triangle yet
            return False

        reg = re.compile(r'\w*\s([A-Z]{2})\svuông\sgóc\s\w*\s*([A-Z]{2})')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        for match in matches:
            height = match[0].upper()
            self.program.set_height(self.context, height[0], height[1])

        return True

    def parse_tri_point(self, sent: str) -> bool:
        if self.context is None: # if not meet triangle yet
            return False

        reg = re.compile(r'điểm ([A-Z]{1}) nằm trong tam giác')
        match = reg.search(sent)
        if match is None:
            reg = re.compile(r'([A-Z]{1}) là một điểm nằm trong tam giác')
            match = reg.search(sent)
            if match is None:
                return False

        p = match.group(1).upper()
        self.program.set_point(self.context, p)

    def parse_ray(self, sent: str) -> bool:
        if self.context is None:
            return False

        from_v, m_v, to_v = None, None, None

        reg = re.compile(r'[Tt]ia ([A-Z]{2}) cắt ([A-Z]{2}) ở ([A-Z]{1})')
        match = reg.search(sent)
        if match is None:
            return False
        from_v = match.group(1).upper()[0]
        m_v = match.group(1).upper()[1]
        to_v = match.group(3).upper()

        self.program.set_ray(self.context, from_v, m_v, to_v)
        
    def parse_edge_eq(self, sent: str) -> bool:

        reg = re.compile(r'([A-Z]{2}) = ([A-Z]{2})( = ([A-Z]{2}))?')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False

        match = matches[0]
        e1 = match[0]
        e2 = match[1]
        e3 = None
        if match[3] != '':
            e3 = match[3]

        #parse value
        reg = re.compile(r'= ([0-9]+)cm')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        e_value = int(matches[0])

        self.program.set_edge(e1, e_value)
        self.program.set_edge(e2, e_value)
        if e3 is not None:
            self.program.set_edge(e3, e_value)
        return True

    def parse_goal(self, sent):
        sent = sent.lower()
        if "tính" in sent:
            self.goal_type = 1
            return True
        if "so sánh" in sent:
            self.goal_type = 2
            return True
        if "chứng tỏ" in sent or "chứng minh" in sent:
            self.goal_type = 3
            return True
        
        reg = re.compile(r'[tT]ìm góc bằng góc ([a-zA-Z]{1,3})')
        match = reg.search(sent)
        if match is not None:
            self.program.add_goal(4 , ("ANGLE", match.group(1).upper()))
            return True
            
        return False
        

    def parse_angle_q(self, sent):
        if self.goal_type == 0:
            return False
        reg = re.compile(r'góc\s+([A-Z]{1,3})')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        if self.goal_type == 1:
            for angle_name in matches:
                self.program.add_goal(self.goal_type , ("ANGLE", angle_name.upper()))
        
        if self.goal_type == 2:
            #self.program.add_goal(self.goal_type , ("ANGLE", angle_name.upper()))
            self.program.add_goal(2 , ("ANGLE", matches[0].upper(), matches[1].upper())) # So sánh

    def parse_relation_1(self, sent):
        if self.goal_type == 0:
            return False
        reg = re.compile(r'([A-Z][a-zA-Z]) song song ([A-Z][a-zA-Z])')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        if self.goal_type == 3:
            for match in matches:
                self.program.add_goal(self.goal_type , Relation("SONG_SONG", Line(match[0]), Line(match[1])))

    def parse_relation_2(self, sent):
        if self.goal_type == 0:
            return False
        reg = re.compile(r'góc ([A-Z]{1,3}).*góc tù')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        if self.goal_type == 3:
            self.program.add_goal(self.goal_type , Relation("GOC_TU", Angle(matches[0])))

    def parse_relation_3(self, sent):
        if self.goal_type == 0:
            return False
        reg = re.compile(r'góc ([A-Z]{3}) = góc ([A-Z]{3})')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        match = matches[0]
        
        self.program.add_goal(self.goal_type , Eq(Angle(match[0]).symb, Angle(match[1]).symb)) # chứng minh




        
        

