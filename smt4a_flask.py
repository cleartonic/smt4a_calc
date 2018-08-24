import smt4a_calc as smt4

from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, BooleanField, IntegerField

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f37d441f29567d441f2b6176b'
  
SKILL_LIST = [(skill,skill) for skill in smt4.SKILL_RAW]
DEMON_LIST = [(demon,demon) for demon in sorted(smt4.DEMON_RAW)]



class Profile:
    def __init__(self, form_data):
        for key in form_data:
            setattr(self,key,form_data[key])        
        skill_list = list(set([self.skill1,self.skill2,self.skill3,self.skill4,self.skill5,self.skill6,self.skill7,self.skill8]))
        if len(skill_list) > 1 and '' in skill_list:
            skill_list.remove('')
        self.skill_list = skill_list
		
class SkillForm(FlaskForm):
    skill1 = SelectField(label='Skill', choices=SKILL_LIST)
    skill2 = SelectField(label='Skill', choices=SKILL_LIST)
    skill3 = SelectField(label='Skill', choices=SKILL_LIST)
    skill4 = SelectField(label='Skill', choices=SKILL_LIST)
    skill5 = SelectField(label='Skill', choices=SKILL_LIST)
    skill6 = SelectField(label='Skill', choices=SKILL_LIST)
    skill7 = SelectField(label='Skill', choices=SKILL_LIST)
    skill8 = SelectField(label='Skill', choices=SKILL_LIST)
    
    target_demon = SelectField(label='Target demon:', choices=DEMON_LIST)
    skill_match_only = BooleanField(label='Strict skill match only:')
    fusion_level = IntegerField(label='Max Fusion Level')
    max_only = BooleanField(label='Highest scoring output only:')
 
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = SkillForm()
	#if form.validate():
    if request.method=='POST':
        p = Profile(form.data)
        p.output_results = smt4.generate_results(p.target_demon, p.skill_list, p.fusion_level,p.skill_match_only,p.max_only)
        # print(p.__dict__)
        return render_template('test.html',form=form, output_results = p.output_results)
    else:
        return render_template('test.html',form=form)
 
if __name__ == "__main__":
    app.run(debug=True)