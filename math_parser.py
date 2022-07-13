from underthesea import word_tokenize, sent_tokenize
from nlp import text_preprocess
import regex as re
from program import Program


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
            self.parse_angle(sent)
            self.parse_bisector(sent)
            # words = sent.split(" ")
            # for i, w in enumerate(words):
            #     self.parse_h_word(i, words)

    # def parse_h_word(self, i, words):
    #     w = words[i]
    #     if w == "tam_giác":
    #         self.parse_triangle(i, words)

    #     if w == "góc":
    #         self.parse_angle(i, words)

    #     if w == "tia_phân" and words[i+1] == "giác":
    #         self.parse_bisector(i, words)

    #     if w == "tia":
    #         self.parse_ray(i, words)

    # def parse_triangle(self, i, words):
    #     if i < len(words) - 1:
    #         tri_name = words[i+1].upper()
    #         self.program.set_triangle(tri_name)
    #         self.context = tri_name

    # def parse_angle(self, i, words):
    #     angle_name, angle_value = None, None
    #     if i < len(words) - 1:
    #         angle_name = words[i+1].upper()
    #     if i < (len(words) - 4) and words[i+2] == "=" and words[i+4] == "độ":
    #         angle_value = words[i+3]

    #     if angle_name is not None:
    #         self.program.set_angle(self.context, angle_name, angle_value)

    # def parse_bisector(self, i, words):
    #     from_v, to_v = None, None
    #     for j in range(i + 1, len(words)):
    #         if words[j] == "góc":
    #             from_v = words[j+1].upper()
    #         if j < len(words) - 3 and words[j] == "cắt" and words[j+2] == "ở":
    #             to_v = words[j+3].upper()
    #     if from_v is not None:
    #         self.program.set_bisector_in(self.context, from_v, to_v)

    def parse_triangle(self, sent: str) -> bool:
        reg = re.compile(r'tam_giác.+([A-Z]{3})\b')
        match = reg.search(sent)
        if match is None:
            return False
        tri_name = match.group(1)
        self.program.set_triangle(tri_name)
        self.context = tri_name
        return True

    def parse_angle(self, sent: str) -> bool:
        if self.context is None: # if not meet triangle yet
            return False

        reg = re.compile(r'góc\s+([A-Z]{1,3})\s*=\s*(\d{2})\b')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        for angle in matches:
            angle_name = angle[0]
            angle_value = angle[1]
            self.program.set_angle(self.context, angle_name, angle_value)

        return True

    def parse_bisector(self, sent: str) -> bool:
        if self.context is None: # if not meet triangle yet
            return False

        reg = re.compile(r'[Tt]ia_phân.+góc\s+([A-Z]{1,3})\s+cắt\s+([A-Z]{2})\s+ở\s+([A-Z]{1})')
        match = reg.search(sent)
        if match is None:
            return False
        from_v = match.group(1)
        to_v = match.group(3)
        self.program.set_bisector_in(self.context, from_v, to_v)

        return True

    def parse_ray(self, sent: str) -> bool:
        from_v, m_v, to_v = None, None, None

        

    def parse_question(self):
        q_sents = sent_tokenize(self.question)
        for sent in q_sents:
            sent = text_preprocess(sent)
            self.parse_goal(sent)
            self.parse_angle_q(sent)

    def parse_goal(self, sent):
        reg = re.compile(r'[Tt]ính.+')
        match = reg.search(sent)
        if match is None:
            return False
        self.goal_type = 1

    def parse_angle_q(self, sent):
        if self.goal_type == 0:
            return False
        reg = re.compile(r'góc\s+([A-Z]{1,3})')
        matches = reg.findall(sent)
        if len(matches) == 0:
            return False
        for angle_name in matches:
            self.program.add_goal(self.goal_type , ("ANGLE", angle_name))




        
        

