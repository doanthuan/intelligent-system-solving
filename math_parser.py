from underthesea import word_tokenize, sent_tokenize
from nlp import text_preprocess

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
            words = text_preprocess(sent)
            for i, w in enumerate(words):
                self.parse_h_word(i, words)

    def parse_h_word(self, i, words):
        w = words[i]
        if w == "tam_giác":
            self.parse_triangle(i, words)

        if w == "góc":
            self.parse_angle(i, words)

        if w == "tia_phân" and words[i+1] == "giác":
            self.parse_bisector(i, words)

    def parse_triangle(self, i, words):
        if i < len(words) - 1:
            tri_name = words[i+1].upper()
            self.program.set_triangle(tri_name)
            self.context = tri_name

    
    def parse_angle(self, i, words):
        angle_name, angle_value = None, None
        if i < len(words) - 1:
            angle_name = words[i+1].upper()
        if i < (len(words) - 4) and words[i+2] == "=" and words[i+4] == "độ":
            angle_value = words[i+3]

        if angle_name is not None:
            self.program.set_angle(self.context, angle_name, angle_value)

    def parse_bisector(self, i, words):
        from_v, to_v = None, None
        for j in range(i + 1, len(words)):
            if words[j] == "góc":
                from_v = words[j+1].upper()
            if j < len(words) - 3 and words[j] == "cắt" and words[j+2] == "ở":
                to_v = words[j+3].upper()
        if from_v is not None:
            self.program.set_bisector_in(self.context, from_v, to_v)

    def parse_question(self):
        q_sents = sent_tokenize(self.question)
        for sent in q_sents:
            words = text_preprocess(sent)
            for i, w in enumerate(words):
                self.parse_q_word(i, words)

    def parse_q_word(self, i, words):
        w = words[i]
        if w == "tính":
            self.goal_type = 1

        if w == "góc" and i < len(words) - 1:
            angle_name = words[i + 1].upper()
            self.program.add_goal(self.goal_type , ("ANGLE", angle_name))



        
        

