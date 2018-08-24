# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 10:09:22 2018

@author: Patrick McMahon
"""

import pandas as pd
import pickle
import itertools
import logging
import coloredlogs

logging.info("Script start.")

coloredlogs.install()

pd.options.mode.chained_assignment = None


### TO DO
#
#
# Set up a collection class for results of a generated query
# Figure out how to connect multiple 'levels' of searches for a final_result (big task)
# Finish building database, somehow figure out how to load special fusions into objects and save (diff format than df_fusions)
#
###


######################## FUNCTIONS #####################################
#
#
#
#
########################################################################
        

def find_demon(demon_name_str,demon_master):
    for i in demon_master:
        if i.name == demon_name_str:
            return i
    logging.info("No matches found for demon "+demon_name_str)

def assign_combinations(demon_name_str,demon_master):
    all_combos = []
    all_combos_names = []
    df_fusion_2 = df_fusion[df_fusion['result_name'] == demon_name_str]
    df_fusion_2.reset_index(inplace=True)
    for index,row in df_fusion_2.iterrows():
        demon1 = find_demon(df_fusion_2['1_name'].iloc[index],demon_master)
        demon2 = find_demon(df_fusion_2['2_name'].iloc[index],demon_master)
        all_combos.append([demon1,demon2])
        all_combos_names.append([demon1.name,demon2.name])
    return all_combos, all_combos_names


def find_scores(dict_list):
    # Argument = a set of skill_dict's to find the overall ResultTree's score
    # Returns a new dictionary
    
    comp_dict_keys = list(dict_list[0].keys())
    comp_dict = dict(zip(comp_dict_keys,[0]*len(comp_dict_keys)))
    
    for key in comp_dict_keys:
        for dict1 in dict_list:
            if dict1[key] == 1:
                comp_dict[key] = 1
    
    return comp_dict

######################## CLASSES #####################################
#
#
#
#
########################################################################


class Demon:  #['race', 'lv', 'name', 'hp', 'mp', 'st', 'dx', 'ma', 'ag', 'lu', 'res_phys', 'res_gun', 'res_fire', 'res_ice', 'res_elec', 'res_force', 'res_light', 'res_dark', 'aff_phys', 'aff_gun', 'aff_fire', 'aff_ice', 'aff_elec', 'aff_force', 'aff_light', 'aff_dark', 'aff_almighty', 'aff_heal', 'aff_debuff', 'aff_buff',  skill_list]
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
        # Initiate demon_qualifier based on recruitable. Will later be used for skill appending
        self.demon_qualifier = ""
        if self.recruitable == 'Y':
            self.demon_qualifier = " (R)"
        self.name_output = self.name + self.demon_qualifier
            
    def find_fusions(self,demon_master):
        self.fusions, self.fusions_names = assign_combinations(self.name,demon_master)  # using the newly assigned self.name, find all combinations and store both the name list and the Demon objects list
        self.fusions.append([self])    # Assigns itself, useful for combo searches later
        self.fusions_names.append([self]) # Assigns itself, useful for combo searches later
    def find_skills(self,skill_list):
        self.skill_dict = dict(zip(skill_list,[0] * len(skill_list))) # Creates a dictionary to store each skill passed and whether its been met or not
        for skill in skill_list:
            if skill in self.skill_list:
                self.demon_qualifier = self.demon_qualifier + " ("+skill+")"
                self.skill_dict[skill] = 1
        self.update_name()
    def update_name(self):
        self.name_output = self.name + self.demon_qualifier
        
class Skill:  # skill_name=skill_name, skill_type=skill_type, mp=mp, desc=desc, target=target, rank=rank, demon_list=demon_list)
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)



class Result:
    # Stores one combination of a final_result demon and all its requirements
    # Each demon stored as a Demon class object
    # The distinction for these Results is that they are set up to be based on a query for requirements (recruitable, skills, etc.)
    
    def __init__(self, final_result, demon_list):  # final_result, [demon_1, demon_2, demon_3...] 
        self.final_result = final_result
        self.demon_list = demon_list
        self.final_result_qualifier = ''
        self.demon_num = len(demon_list)
        self.recruit_score_max = self.demon_num # Technically duplicative, replicated for ease
        self.recruit_score_num = 0          # A bit tbd on how scores work. 
        self.recruit_score = 0
        self.skill_score_num = 0
        
        # Find fusion limit
        # Fusion limit is defined as the min among all demons in the result, and the final demon
        # One theoretically could argue it should just be the final result
        # But it quickly will turn into many demons in the formulas that are very high level and aren't realistic
        limit_list = []
        for demon in self.demon_list:
            limit_list.append(demon.lv)
        limit_list.append(final_result.lv)
        self.fusion_limit = min(limit_list)
        
        self.scored = False
    def find_skill_score(self):
        if self.scored:
            pass
        else:
            # Compile all skill dicts from demons
            demon_skill_dicts = []
            for demon in self.demon_list:
                demon_skill_dicts.append(demon.skill_dict)
            # Add final_result's skill list
            demon_skill_dicts.append(self.final_result.skill_dict)
            
            self.skill_dict = find_scores(demon_skill_dicts)  # This represents the final skills and if they've been met, all in a dict 
            self.skill_score_max = len(self.skill_dict.keys()) # Skill num based on keys in the dict


            # Check if at least one skill has been met, and get skill_score_num
            self.skill_match = False
            for skill in self.skill_dict.values():
                if skill == 1:
                    self.skill_match = True              # As long as one skill is matched, output will be generated. 
                    self.skill_score_num = self.skill_score_num + 1
                    

            # Get recruitable score
            for demon in self.demon_list:       # For every demon in the fusion requirement for final_result        
                if demon.recruitable == 'Y':
                    self.recruit_score_num = self.recruit_score_num + 1
            if self.final_result.recruitable == 1:              # And also the final_demon
                self.recruit_score_num = self.recruit_score_num + 1


            # Generate demon list str, which is collected from the demons' name_output
            self.demon_list_str = []
            for demon in self.demon_list:
                self.demon_list_str.append(demon.name_output)
            self.final_result_str = self.final_result.name_output

            
            if self.demon_num == 1:
                req_str = ('[%s] (No Fusion)'+' → '+self.final_result_str) % tuple(self.demon_list_str)
            elif self.demon_num == 2:
                req_str = ('[%s x %s]'+' → '+self.final_result_str) % tuple(self.demon_list_str)
            elif self.demon_num == 3:
                req_str = ('[%s x %s x %s]'+' → '+self.final_result_str) % tuple(self.demon_list_str)
            elif self.demon_num == 4:
                req_str = ('[%s x %s x %s x %s]'+' → '+self.final_result_str) % tuple(self.demon_list_str)
            else:
                logging.info("ERROR! More than 4 demons in fusion list?")
                logging.info(self.demon_list_str, self.demon_num)

            self.skill_output = req_str
            self.skill_score = self.skill_score_num / self.skill_score_max
            self.recruit_score = self.recruit_score_num / self.recruit_score_max
            self.scored = True
            
        
class ResultTree:
    
    # The purpose of a ResultTree is to store one combination for a result demon two level downs.
    # For example: Mot → [one of  73 combinations of Mot] → [One possible combinations for one those 73]
    # All the Results objects are stored in a master list, irrespective of what the demons are along the way
    
    # Each element represents the combination of results that are needed. So, at least 2 Result objects. Each element will need to be score independently.
    
    
    def __init__(self, final_result, results_list):
        self.final_result = final_result
        self.results_list = results_list
        self.scored = False                 # This is set to zero until the score_results function is called. Can't print results before score_results is called


        # Upon init, set up string for final fusion
        demon_list_str = []
        for result in self.results_list:
            demon_list_str.append(result.final_result.name)
        self.demon_num = len(demon_list_str)
        if self.demon_num == 1:
            self.final_str = ('[%s] → '+self.final_result.name) % tuple(demon_list_str)
        elif self.demon_num == 2:
            self.final_str= ('[%s x %s] → '+self.final_result.name) % tuple(demon_list_str)
        elif self.demon_num == 3:
            self.final_str = ('[%s x %s x %s] → '+self.final_result.name) % tuple(demon_list_str)
        elif self.demon_num == 4:
            self.final_str = ('[%s x %s x %s x %s] → '+self.final_result.name) % tuple(demon_list_str)
        else:
            logging.info("ERROR! More than 4 demons in fusion list?")

    

        # Upon init, find total demons for fusing. Used for scoring/sorting results
        
        self.demon_score = 0
        for result in results_list:
            self.demon_score = self.demon_score + result.demon_num
        
        
        # Upon init, set fusion_limit based on the max of all results within the tree:
        
        all_limits = []
        for result in results_list:
            all_limits.append(result.fusion_limit)
        self.fusion_limit = max(all_limits)
        
        
        
        # Upon init, hash the absolute demon list
        # THIS IS WHERE THERE'S MOST LIKELY FOR RESULTTREES TO GET LOST
        # This is naturally filtering any combination of demons used
        # The goal is to get rid of duplicates, which it will
        # But it may cut out weird pathings like using the same demon twice 
        #
        # Update: Never implemented. Delete if necessary...
        
        all_demons = []
        all_demons.append(self.final_result)
        for i in self.results_list:
            all_demons.append(i.final_result)
        for i in self.results_list:
            for demon in i.demon_list:
                all_demons.append(demon)

        all_demons = list(set(all_demons))
        self.all_demons = all_demons
        self.hash = hash(str(all_demons))
        
            
    def score_results(self):
        
        # Check skills:
        skill_dict_compile = []                 # going to be passed into find_scores to find the overall skill score of the ResultTree
        for result in self.results_list:        # first generate skill checks per result
            skill_dict_compile.append(result.skill_dict)
        self.skill_dict_score = find_scores(skill_dict_compile)
        self.skill_score_num = sum(list(self.skill_dict_score.values()))
        self.skill_score_max = len(self.skill_dict_score.values())
        self.skill_score =  self.skill_score_num / self.skill_score_max
        self.scored = True
        
        # Check recruitable:
        d_list = []
        r_num = 0
        for result in self.results_list:        # first generate skill checks per result
            r_num = r_num + result.recruit_score_num
            for d in result.demon_list:
                d_list.append(d.name)
        self.recruit_score_max = len(d_list)
        self.recruit_score_num = r_num
        self.recruit_score = self.recruit_score_num / self.recruit_score_max
        
        # Calculate end score & output str
        if self.scored:
            temp = []
            for i in self.results_list:
                if 'reported' not in i.skill_output:
                    temp.append(i.skill_output)
            self.combination_str = temp
            self.output_str = "RECRUIT Score: "+str(self.recruit_score_num)+" SKILL score: "+str(self.skill_score_num)+" "+self.final_str+"\n"
            if len(self.combination_str) > 0:
                for i in self.combination_str:
                    self.output_str = self.output_str+i+"\n"
            
class ResultCluster:
    
    # The purpose of a ResultCluster is to store all the ResultTrees that can result in a final_result 
    # Here, the collection of ResultTrees will be sorted and printed
    
    # The rationale for all the ResultTrees together, regardless of what demons appear at various stages.
    #   It shouldn't matter how you get to the result_demon, just that you get there with the skills along the way,
    #   and that the skill score / recruitable score will dictate its viability
            
    def __init__(self, final_result, resulttree_list):
        self.final_result = final_result
        self.resulttree_list = resulttree_list
        self.output_results = []

    def print_results(self,save_only=False,max_only=False):
        
        # First compile stats about the results list
        
        
        trees_skill_scores = []
        trees_recruit_scores = []
        trees_demon_scores = []
        for tree in self.resulttree_list:
            trees_skill_scores.append(tree.skill_score)
            trees_recruit_scores.append(tree.recruit_score)
            trees_demon_scores.append(tree.demon_score)
        self.skill_scores = sorted(list(set(trees_skill_scores)))
        self.recruit_scores = sorted(list(set(trees_recruit_scores)))
        self.demon_scores = sorted(list(set(trees_demon_scores)))[::-1]
        
#        logging.info("SKILL "+str(self.skill_scores))
#        logging.info("RECRU "+str(self.recruit_scores))
#        logging.info("DEMON "+str(self.demon_scores))

        if max_only:
            # For now, use top 2 possibilities.
            # Also for now, ignore actually generating max from demon_scores. Although interesting to slice results this way,
            #     actually filtering on the top two often causes no results for the 'strongest' category of recruit/skill
            # Generating a true "max power" across all three fields seems tough................
                        
            if (len(self.skill_scores) >= 2):
                max1_skill_scores = max(self.skill_scores)
                self.skill_scores.remove(max1_skill_scores)
                max2_skill_scores = max(self.skill_scores)
                self.skill_scores = [max1_skill_scores, max2_skill_scores]
            else:
                pass
            
            if (len(self.recruit_scores) >= 2):
                max1_recruit_scores = max(self.recruit_scores)
                self.recruit_scores.remove(max1_recruit_scores)
                max2_recruit_scores = max(self.recruit_scores)
                self.recruit_scores = [max1_recruit_scores, max2_recruit_scores]
            else:
                pass
            
#            if (len(self.demon_scores) >= 2):
#                max1_demon_scores = max(self.demon_scores)
#                self.demon_scores.remove(max1_demon_scores)
#                max2_demon_scores = max(self.demon_scores)
#                self.demon_scores = [max1_demon_scores, max2_demon_scores]
#            else:
#                pass
            
            
            
            
            
            # Old method, true max for each category. Often reports blank because it idealistically takes the max from any slice            
#            self.skill_scores = [max(self.skill_scores)]
#            self.recruit_scores = [max(self.recruit_scores)]
#            self.demon_scores = [min(self.demon_scores)]
            
        # Then print results
        if save_only:
            with open('output/file.txt','w',encoding='utf-8') as f:
                f.write("")
            for skill_score_rank in self.skill_scores:
                for demon_score_rank in self.demon_scores:
                    for recruit_score_rank in self.recruit_scores:
                        temp_outputs = []
                        for tree in self.resulttree_list:
                            if tree.skill_score == skill_score_rank and tree.recruit_score == recruit_score_rank and tree.demon_score == demon_score_rank:
                                temp_outputs.append(tree.output_str)
                        if len(temp_outputs) > 0:
                            with open('output/file.txt','a',encoding='utf-8') as f:
                                f.write("===============================================\n")
                                f.write("SKILL SCORE: "+str(skill_score_rank)+"\n")
                                f.write("RECRUIT SCORE: "+str(recruit_score_rank)+"\n")
                                f.write("DEMON #: "+str(demon_score_rank)+"\n")
                                f.write("===============================================\n")
                                for i in temp_outputs:
                                    f.write(i)
        else:
            for skill_score_rank in self.skill_scores:
                for demon_score_rank in self.demon_scores:
                    for recruit_score_rank in self.recruit_scores:
                        temp_outputs = []
                        for tree in self.resulttree_list:
                            if tree.skill_score == skill_score_rank and tree.recruit_score == recruit_score_rank and tree.demon_score == demon_score_rank:
                                temp_outputs.append(tree.output_str)
#                        if len(temp_outputs) > 0:
#                            logging.info("===============================================\n")
#                            logging.info("SKILL SCORE "+str(skill_score_rank)+"\n")
#                            logging.info("DEMON # SCORE "+str(demon_score_rank)+"\n")
#                            logging.info("RECRUIT SCORE "+str(recruit_score_rank)+"\n")
#                            logging.info("===============================================\n")
#                            for i in temp_outputs:
#                                logging.info(i)
                        if len(temp_outputs) > 0:
                            self.output_results.append("===============================================\n")
                            self.output_results.append("SKILL SCORE: "+str(skill_score_rank*100)+"%\n")
                            self.output_results.append("RECRUIT SCORE: "+str(recruit_score_rank*100)+"%\n")
                            self.output_results.append("DEMON #: "+str(demon_score_rank)+"\n")
                            self.output_results.append("===============================================\n")
                            for i in temp_outputs:
                                self.output_results.append(i)


######################## INIT  #####################################
#
#
#
#
########################################################################


SKILL_RAW = ["","5.67 Billion Hands","Acid Breath","Adaptive Tactics","Agi","Agidyne","Agilao","Akasha Arts","Alluring Banter","Ally Counter","Ally Retaliate","Almighty Pleroma","Amrita","Andalusia","Antichthon","Attack Knowhow","Axel Claw","Babylon Goblet","Bad Company","Beastly Reaction","Berserker God","Bind Voice","Binding Claw","Blade of Terror","Blank Bullet","Blast Arrow","Blight","Blink of Death","Blood Ritual","Bloody Glee","Bouncing Claw","Breath","Bufu","Bufudyne","Bufula","Chakra Walk","Charge","Chariot","Cold World","Combat Tara","Concentrate","Cough","Counter","Critical Eye","Critical Wave","Damascus Claw","Dance of Mara","Dark Grudge","Dark Pierce","Dark Pleroma","Dark Sword","Dazzle Ray","Deadly Wind","Death Lust","Death's Door","Debilitate","Dekaja","Dekunda","Desperate Hit","Dia","Diarahan","Diarama","Die for Me!","Doping","Dormina","Draconic Reaction","Drain Dark","Drain Elec","Drain Fire","Drain Force","Drain Gun","Drain Ice","Drain Light","Drain Phys","Dream Fist","Dream Needle","Dream Raga","Earthquake","Eat Whole","Elec Pierce","Elec Pleroma","Endure","Enduring Cheer","Enduring Soul","Energy Drain","Enlightenment","Estoma","Eternal Rest","Evil Melody","Evil Shine","Fang Breaker","Fatal Sword","Fear Darkness","Fire Breath","Fire of Lethargy","Fire of Sinai","Fire Pierce","Fire Pleroma","Floral Gust","Fog Breath","Force Pierce","Force Pleroma","Frenzied Chomp","Glacial Blast","God's Bow","Gram Slice","Grand Tack","Great Logos","Growing Hate","Gun Pierce","Gun Pleroma","Gungnir","Hades Blast","Hama","Hamaon","Hard Worker","Haunting Rhapsody","Head Crush","Heal Pleroma","Healing Knowhow","Heat Wave","Heaven's Bow","Hell Thrust","Hellish Brand","Hellish Mask","High Dark Pleroma","High Elec Pleroma","High Fire Pleroma","High Force Pleroma","High Gun Pleroma","High Heal Pleroma","High Ice Pleroma","High Light Pleroma","High Phys Pleroma","Holy Wrath","Ice Age","Ice Breath","Ice Pierce","Ice Pleroma","Imposing Stance","Infernal Hail","Invitation","Iron Judgment","Javelin Rain","Judgment","Judgment Light","King Bufula","Life Aid","Life Bonus","Life Drain","Life Gain","Life Surge","Light Devourer","Light Life Aid","Light Mana Aid","Light Pierce","Light Pleroma","Loyalty Slash","Lullaby","Lunge","Luster Candy","Mabufu","Mabufudyne","Mabufula","Madness Nails","Madness Needle","Magaon","Magic Torrent","Mahama","Mahamaon","Makajam","Makajamaon","Makakaja","Makarabreak","Makarakarn","Mamudo","Mamudoon","Mana Aid","Mana Bonus","Mana Gain","Mana Surge","Maragi","Maragidyne","Maragion","Marin Karin","Mazan","Mazandyne","Mazanma","Mazio","Maziodyne","Mazionga","Me Patra","Media","Mediarahan","Mediarama","Megaton Press","Megiddo Ark","Megido","Megidola","Megidolaon","Mist Rush","Mortal Jihad","Mudo","Mudoon","Myriad Arrows","Needle Shot","Needlestorm","Nihil Claw","Null Dark","Null Elec","Null Fire","Null Force","Null Gun","Null Ice","Null Light","Null Mind","Null Nerve","Null Phys","Oni-Kagura","Pandemic Bomb","Panic Voice","Patra","Pestilence","Phys Pierce","Phys Pleroma","Poisma","Poison Breath","Poison Claw","Posumudi","Power Punch","Pulinpa","Purple Smoke","Raging Blizzard","Raging Hellfire","Raging Lightning","Raging Tempest","Ragnarok","Rakukaja","Rakunda","Rapid Needle","Recarm","Recarmdra","Rending Claws","Repel Dark","Repel Elec","Repel Fire","Repel Force","Repel Gun","Repel Ice","Repel Light","Repel Phys","Resist Dark","Resist Elec","Resist Fire","Resist Force","Resist Gun","Resist Ice","Resist Light","Resist Phys","Retaliate","Riot Gun","Ruinous Brand","Sabbatma","Salvation","Samarecarm","Scratch Dance","Sea of Chaos","Self-Righteous Vow","Severe Judgment","Sexy Dance","Shibaboo","Shivering Taboo","Shock","Silent Prayer","Smile Charge","Snake's Fangs","Soul Divide","Soul Drain","Spirit Drain","Spring of Life","Stun Needle","Stun Needles","Sukukaja","Sukunda","Tarukaja","Tarunda","Tathlum Shot","Taunt","Tetanus Cut","Tetrabreak","Tetraja","Tetrakarn","Thunder Gods","Thunder Reign","Titanomachia","Toxic Sting","Trafuri","Trisagion","True Zandyne","True Ziodyne","Vengeful Thunder","Venomous Raga","Victory Cry","War Cry","Warding Shout","Will of Flame","Will of Frost","Will of Thunder","Will of Wind","Wind Breath","Workaholic","Zan","Zandyne","Zanma","Zio","Ziodyne","Zionga"]

DEMON_RAW = ["","Katakirauwa","Slime","Goblin","Sudama","Centaur","Caladrius","Legion","Mandrake","Decarabia","Onmoraki","Fuxi","Fomorian","Kabuso","Nadja","Strigoii","Pele","Garrote","Jack the Ripper","Porewit","Erthys","Dwarf","Gremlin","Vodyanik","Zhu Tun She","Bilwis","Leanan Sidhe","Mamedanuki","Pixie","Hamsa","Angel","Dybbuk","Hooligan","Kaso","Sandman","Fortuna","Chagrin","Mothman","Preta","Shan Xiao","Aeros","Agathion","Hua Po","Moh Shuvuu","Napaea","Melchom","Heqet","Makara","Oni","Tam Lin","Shiisaa","Morax","Spriggan","Toubyou","Suparna","Apsaras","Mermaid","Daphne","Aquans","Gu Huo Niao","Ippon-Datara","Koppa Tengu","Knocker","Peallaidh","Strix","Zombie Cop","Hathor","Archangel","Apis","Ictinike","Mokoi","Obariyon","Dzelarhons","Azumi","Itsumade","Naga","Poltergeist","Flaemis","Bifrons","Inugami","Jack Frost","Patrimpas","Mithras","Take-Minakata","Bai Suzhen","Chupacabra","Ubu","Ame no Uzume","Kwancha","Lham Dearg","Night Stalker","Tangata Manu","Kamapua'a","Incubus","Mou-Ryo","Nata Taishi","Nozuchi","Shikome","Phoenix","Ogun","Gnome","Halphas","Karasu Tengu","Pabilsag","Parvati","Camazotz","Baphomet","Momunofu","Pyro Jack","Quicksilver","Principality","Chironnupu","Horkos","Jueyuan","Senri","Stonka","Sedna","Kanbari","Gucumatz","Kuda","Tattooed Man","Sylph","Baldur","Basilisk","Kikimora","Vouivre","Narcissus","High Pixie","Yurlungur","Dis","Myrmecolion","Qing Niugai","Thoth","Okuninushi","Hairy Jack","King Frost","Tuofei","Wendigo","Yuki Jyorou","Tsuchigumo","Inferno","Kelpie","Skogsra","Zhen","Ares","Undine","Churel","Ose","Yamawaro","Brigid","Power","Makami","Lilim","Raijuu","Vidofnir","Mayahuel","Inti","Sukuna-Hikona","Okiku-Mushi","Corpses","Clotho","Harpy","Nekomata","Setanta","Hariti","Yoshitsune","Salamander","Balor","Kikuri-Hime","Tonatiuh","Mad Gasser","Mishaguji","Titan","Yomotsu-Ikusa","Enku","Hare of Inaba","Orias","Rakshasa","Shiwanna","Wicker Man","Medusa","Kaiwan","Kingu","Nue","Scathach","Tlaloc","Prometheus","Kaiming Shou","Black Frost","Kushinada-Hime","Gryphon","Diana","Dionysus","Lachesis","Virtue","Zaccoum","Thunderbird","Frost Ace","Jeanne D'Arc","Gurr","Asura","Hel","Kin-Ki","Kurama Tengu","Valkyrie","Ishtar","Kukunochi","Airavata","Arachne","Silky","Macabre","Manticore","Ogre","Patriot","Succubus","Chimera","Tlaltecuhtli","Atropos","Nebiros","Pachacamac","Ouroboros","Illuyanka","Mushussu","Rukh","Lord Nandou","Alraune","Hsing-Hsing","Sarasvati","Xiuhtecuhtli","Lanling Wang","Hitokoto-Nushi","Alice","Anzu","Fuu-Ki","Ghoul","Chernobog","Zhong Kui","Futotama","Cu Chulainn","Grendel","Orcus","Pallas Athena","Orochi","Asherah","Dominion","Yatagarasu","Catoblepas","Orthrus","Vivian","Osiris","Ukano Mitama","Dantalian","Wild Hunt","Lailah","Haoma","Pisaca","Sui-Ki","Zouchouten","Take-Mikazuchi","Sleipnir","Tiamat","Zhu Yin","Hagen","Da Peng","Kresnik","Taraka","Tlazolteotl","Wu Kong","Arahabaki","Persephone","Loki","Dormarth","Gemori","Lorelei","Taotie","Ometeotl","Isis","Aramisaki","Cabracan","Anubis","Gui Xian","Koumokuten","Kinmamon","Niddhoggr","Victor","Long","Gogmagog","Jarilo","Master Therion","Queen Mab","Baihu","Siegfried","Girimehkala","Peri","Throne","Anat","Feng Huang","Abaddon","Dakini","Guedhe","Murmur","Oberon","Ammut","Berserker","Taowu","Yggdrasil","Jikokuten","Oumitsunu","Huoniao","Ym","Beiji-Weng","Black Maria","Hanuman","Kudlak","Pendragon","Mahamayuri","Quetzalcoatl","Kanseiteikun","Alciel","Israfel","Barong","Adramelech","Hekatoncheires","Rangda","Norn","Azazel","Barbatos","Cerberus","Fenrir","Titania","Bishamonten","Belial","Erlkonig","Hresvelgr","Python","Cernunnos","Cherub","Sphinx","Yaksha","Garuda","Kama","Ganesha","Heimdall","Lucifuge","Pales","Skadi","Shax","Attis","Rama","Vetala","Hachiman","Marishiten","Fafnir","Kali","Tzitzimitl","Demonee-Ho","Samyaza","Ixtab","Azrael","Lakshmi","Tenkai","Maya","Kartikeya","Huang Long","Ongyo-Ki","Baal","Xi Wangmu","Amaterasu","Beelzebub","Seth","Thor","Kangiten","Tokisada","Nergal","Surt","Kazfiel","Izanami","Apsu","David","Tezcatlipoca","Angel White Wings","Maitreya","Botis","Susano-O","Alilat","Odin","Sraosha","Huang Di","Krishna","Chi You","Matador","Vasuki","Mot","White Rider","Samael","Aniel","Inanna","Red Rider","Mara","Mastema","Black Rider","Seraph","Demiurge","Shiva","Pale Rider","Mitra-Buddha","Trumpeter","Metatron","Merkabah","Lucifer","Mother Harlot","Satan"]

logging.info("Init start.")

if False:                
    # Load tables
    df_skills = pd.read_excel('data/skills.xlsx')
    df_fusion = pd.read_excel('data/fusion.xlsx')                
    df_bestiary = pd.read_excel('data/bestiary.xlsx')
                    
    # Initiate results
    #results_zero = Results_levelzero(filter_level_zero)
    #results_one = Results_levelone(filter_level_one)       
    
    
    # The below is a pre-calculated set, saved with pickle. Can re-run again as necessary (as db gets updated). 
    # To change, swap 'if False' to 'if True', run the preparer, then switch back. 
    
    
    # Build skill classes, stored in skills_master list
            
    
    skills_master = []
    for skill_lookup in df_skills['name'].unique().tolist():
        demon_list = df_skills.loc[df_skills['name'] == skill_lookup]['demon_name'].unique().tolist()
        entry = df_skills.loc[df_skills['name'] == skill_lookup].iloc[0]
        skill_type, skill_name, mp, desc, target, rank = entry[1], entry[2], entry[3], entry[4], entry[5], entry[6]
        # skills_master.append(Skill(skill_name, skill_type, mp, desc, target, rank, demon_list))
        skills_master.append(Skill(skill_name=skill_name, skill_type=skill_type, mp=mp, desc=desc, target=target, rank=rank, demon_list=demon_list))
        
    pickle.dump( skills_master, open( "data/skills.p", "wb" ) )
    pickle.dump( [df_skills,df_fusion,df_bestiary], open( "data/tables.p", "wb" ) )
    
else:
    skills_master = pickle.load( open( "data/skills.p", "rb" ) )
    [df_skills,df_fusion,df_bestiary] = pickle.load( open( "data/tables.p", "rb" ) )


# Build list of recruitable demons
recruitable_demons = df_bestiary[df_bestiary['recruitable'] != '[n/a]']['name'].unique().tolist()




    # Build demons, stored in demon_master

demon_master = []
for demon_lookup in df_bestiary['name'].unique().tolist():
    # build from skills
    skill_list = df_skills.loc[df_skills['demon_name'] == demon_lookup]['name'].unique().tolist()
    
    # build from bestiary
    df = df_bestiary.loc[df_bestiary['name'] == demon_lookup]
    if not df.empty:
        stat_list = df.iloc[0].to_dict()  # temp dict for all demon stats
        stat_list['skill_list'] = skill_list # add skill_list
        demon_master.append(Demon(**stat_list)) # add new demon to master with stats & skills
        













############### TEST AREA ######################

def generate_results(target_demon_input,skills_input,fusion_level,skill_match_only,max_only):
    logging.info("Test area start.")
    global demon_master
    
    sk = skills_input
    fusion_limit = fusion_level
    pure_skill_match = skill_match_only
    save_only_flag = True
    max_only_flag = max_only
    
    logging.info("Scoring demons on skill list...")
    
    for demon in demon_master:
        demon.find_skills(skills_input)
        demon.find_fusions(demon_master)
    logging.info("Scored demons on skill list.")

    d = find_demon(target_demon_input,demon_master)


    logging.info("Starting fusion combo generation...")
    
    
    # Data validation/cleanup
    final_master = []
    if sk == ['']:
        pure_skill_match = False
    
    # Default to target demon level if nothing given 
    if type(fusion_limit) != int or fusion_limit  <= 0:
        fusion_limit = d.lv
    
    
    
    
    ##
    #
    # Probably make the below a function of a ResultCluster to generate all of this. 
    #
    ##
    
    
    for i, final_combo in enumerate(d.fusions):
        #logging.info("Final combo #: "+str(i)+"...")
        final_combo_perm = []
        combo_len = len(final_combo)
        for demon_num in range(combo_len):
            demon = final_combo[demon_num]
            temp_fusions = []
            for fusion in demon.fusions:
                r = Result(demon,fusion)
                r.find_skill_score()    # Upon generation, find the skill score for the whole result
                if fusion_limit >= r.fusion_limit: # Check for fusion_limits. If the fusion_limit is higher than the result's fusion_limit, then add to the list. Otherwise discard
                    temp_fusions.append(r)  # add to list for permutation
                else:
                    del(r) # delete from memory
                    
            final_combo_perm.append(temp_fusions)
        final_master.append(list(itertools.product(*final_combo_perm)))
    logging.info("Fusion combo generation complete.")
    
    logging.info("List generation start...")
    master2 = []
    for i in final_master:
        for y in i:
            master2.append(y)
    
    
    # After result_trees are generated, they must be checked for flags. 
    
    result_tree = []        
    for i in master2:
        rt = ResultTree(d,i)
        # Fusion limit flag: Only add results that are under the fusion level limit
        if fusion_limit >= rt.fusion_limit:
            result_tree.append(rt)
    
    # for debug only - set up one rt object
    try:        
        rt = result_tree[0]
    except:
        logging.info("No rt results. Error on debug rt creation.")
    
    logging.info("List generation complete.")
    
    if len(result_tree) > 0:
        #result_tree = result_tree[300:300]
        logging.info("Result tree scoring start...")
        
        result_tree2 = []
        for result_tree_instance in result_tree:  # result_tree_instance = 1 item. result_tree and result_tree2 are lists
            result_tree_instance.score_results()
            if pure_skill_match:
                # Pure skill match flag: Only add results that fully meet the skill criteria. E.g., if not skills present at all, discard entirely
                # Also only applies when the skill list is populated. Otherwise, ignore, because nothing will match and it'll return blanks. 
                
                if result_tree_instance.skill_score == 1:
                    result_tree2.append(result_tree_instance)
                    
        if pure_skill_match:
            result_tree = result_tree2[:]
        logging.info("Result tree scoring complete.")
        
        logging.info("Results generation start...")
        
        rc = ResultCluster(d,result_tree)
        rc.print_results(save_only=save_only_flag,max_only=max_only_flag)
        
        logging.info("Results generation complete.")
        return rc.output_results
    else:
        logging.info("No matches. Results not generated.")
        
        
####### NEED TO NOT RUN THIS & THE PICKLING FOR USE WITH FLASK        
        

if True:
    target_demon_input = 'Valkyrie'
    skills_input = ['Agilao']
    fusion_level = -1
    skill_match_only = True
    max_only = False
            
    results = generate_results(target_demon_input,skills_input,fusion_level,skill_match_only,max_only)