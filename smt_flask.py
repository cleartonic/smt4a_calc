import smt_calc as smt

from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, BooleanField, IntegerField

application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
application.config.from_object(__name__)
application.config['SECRET_KEY'] = '7d441f37d441f29567d441f2b6176b'
  
SKILL_LIST = [(skill,skill) for skill in smt.SKILL_RAW]
DEMON_LIST = [(demon,demon) for demon in sorted(smt.DEMON_RAW)]



class Profile:
    # Profile represents every time the user submits a form, what is entered
    
    def __init__(self, form_data):
        for key in form_data:
            setattr(self,key,form_data[key])        
        skill_list = list(set([self.skill1,self.skill2,self.skill3,self.skill4,self.skill5,self.skill6,self.skill7,self.skill8]))
        if len(skill_list) > 1 and '' in skill_list:
            skill_list.remove('')
        self.skill_list = skill_list
        
        demon_filter_list = list(set([self.filter_demon1,self.filter_demon2,self.filter_demon3,self.filter_demon4]))
        if len(demon_filter_list) > 1 and '' in demon_filter_list:
            demon_filter_list.remove('')
        self.demon_filter_list  = demon_filter_list
		
class SkillForm(FlaskForm):
    skill1 = SelectField(label='Skill', choices=SKILL_LIST)
    skill2 = SelectField(label='Skill', choices=SKILL_LIST)
    skill3 = SelectField(label='Skill', choices=SKILL_LIST)
    skill4 = SelectField(label='Skill', choices=SKILL_LIST)
    skill5 = SelectField(label='Skill', choices=SKILL_LIST)
    skill6 = SelectField(label='Skill', choices=SKILL_LIST)
    skill7 = SelectField(label='Skill', choices=SKILL_LIST)
    skill8 = SelectField(label='Skill', choices=SKILL_LIST)
    
    filter_demon1 = SelectField(label='Filter demons:', choices=DEMON_LIST)
    filter_demon2 = SelectField(label='Filter demons:', choices=DEMON_LIST)
    filter_demon3 = SelectField(label='Filter demons:', choices=DEMON_LIST)
    filter_demon4 = SelectField(label='Filter demons:', choices=DEMON_LIST)
    
    target_demon = SelectField(label='Target demon:', choices=DEMON_LIST)
    skill_match_only = BooleanField(label='Strict skill match only:',default=True)
    strict_filter = BooleanField(label='Strict filtering on all input filter demons:')
    fusion_level = IntegerField(label='Max Fusion Level (blank defaults to target demon level)')
    max_trees = IntegerField(label='Max trees',default=10)
    max_tree_results = IntegerField(label='Max tree results',default=10)
    max_only = BooleanField(label='Highest scoring output only:',default=True)
 
 
 
@application.route("/", methods=['GET', 'POST'])
def hello():
    form = SkillForm()
	#if form.validate():
    if request.method=='POST':
        p = Profile(form.data)
        rc = smt.ResultCluster(p.target_demon, p.skill_list, p.fusion_level,p.skill_match_only,p.max_only,p.demon_filter_list,p.strict_filter)
        rc.generate_results()
        
        # Take score_dict, which is in: { OVERALL SCORE : [list of skill/recruit/demon] } format
        # And convert to:
        # { OVERALL SCORE : ( [list of skill/recruit/demon], [RT_LIST] ) } 
        # The reason for the original OVERALL SCORE is to have the ordering of the magnitude (highest scores first)
        # out
        
        
        if rc.result_failure:
            return render_template('index.html',form=form)
        else:
            output_scores = rc.find_matching_scores()
            output_scores = {k: v for k, v in output_scores.items() if k < p.max_trees }
            total_results = rc.total_results
            total_filtered_results = rc.total_filtered_results
            del(rc)
            return render_template('index.html', total_results=total_results, total_filtered_results=total_filtered_results,form=form, output_scores = output_scores, max_trees = p.max_trees, max_tree_results = p.max_tree_results)
    else:
        return render_template('index.html',form=form)
 
    
@application.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message))

    return dict(mdebug=print_in_console)
    
if __name__ == "__main__":
    application.jinja_env.cache = {}
    application.run(debug=True)