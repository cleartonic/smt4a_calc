# SMT Reverse Fusion Calculator

#### A tool to help identify target demons by dynamically searching for fusions based on matching skills, recruitability, and demon number.
#### <a href="http://cleartonic.pythonanywhere.com/" target="_blank">Link to browser interface</a>

### Current version:
- Supports SMT4: Apocalypse (English)

### Next versions:
- Implement 3/4 fusion requirement demons (functional as of now, but generates too many combinations which crashes the program. Need to smart filter somehow)
- Support demon information/graphics in the interface, such as recruit locations, levels, etc.

![image](diagram.png?raw=true "image")

### Premise:
Input a target demon (what you're attempting to fuse), and what skills you'd like. The calculator will generate all possible combinations '2 levels down', meaning all combinations that directly create the target demon, then all combinations that create each one of those combinations. This is referred to as a "result tree", just one of the many possible paths to create the final demon. 

All final result trees are scored on three criteria, in the following priority order:
- Skills: higher score for most matching skills relative to the query
- Recruitable: higher score for % of demons able to be recruited rather than fused 
- Demon: # of demons in the fusion

The output will sort these results their scores above. Each row shows the first combination down, then clicking on the row expands to all the combinations with the fusion demons and their skills. (note: The "(R)" indicates that the demon is recruitable)

For a basic, fast example, try searching Target demon "Pele", and uncheck "highest scoring output". This will return all combinations of Pele. Then try filtering for the skill "Mudo" and run again. Then select "highest scoring output", and naturally only the highest score (100/100/3 for skill/recruit/demon) will be shown. 

This program can be computationally intensive at times - some demons have an incredible amount of combinations (for example, a mid-50s demon such as "Illuyanka" has over 2 million ways to be created with the above '2 levels down' system.)


### Calculator arguments:

#### Target demon - The final desired demon 
Skill - Up to 8 skills can be added. Each result tree will be scored individually based on whether or not the skills appear in the tree.
- Setting the "Strict skill match only" flag will require all skills selected to be present in the tree, otherwise it is rejected from the output
- Not setting the "Strict skill match only" flag will score all result trees based on how many of the desired skills appear in the result tree. For example, if the desired skills are "Hama", "Mudo", and "Dia", and a result tree's demons only have "Hama" and "Dia", the score will be 66%

#### Filter demons - Up to 4 demons can be added. These will allow for filtering the results 
- Setting the 'strict filtering on all input filter demons" flag requires all filter demons to be present in the result tree
- Not setting the 'strict filtering on all input filter demons" flag, but setting any number (1-4) of filtered demons, will show only result trees where at least 1 of the demons is present

#### Max fusion level - This is the fusion level of the player character, which limits which fusions are available. 
- Default fusion level is set to the target demon, if none is entered. 
- Fusion level 99 assumes all fusions are available
- Fusions are assumed to be limited to the max of all demons in the fusion. Theoretically, the player could grind demons past their fusion limit, but this system doesn't accommodate this, and assumes the player can recruit/make demons up to their fusion level. If this is a problem, just manually increase the fusion limit. 

#### Max trees - The number of trees to display. 
Each tree represents the first level down to make the target demon, at a specific score (based on the whole tree's fusions). Note that if the 'highest scoring output only' flag is set, only the top scoring trees will appear, which will drastically decrease the number of trees (and also speed up processing). 

#### Max tree results - The number of results in the expanded view for every result tree. 
When you click on the results bar for a given result tree, how many entries appear. This is set to 10, because most result trees can have a huge amount. This can be set to any number as the limit, but generation may take longer. Further, use filter demons if looking for a specific demon among the trees. 

#### Flags:
- "Strict skill matching only" and "Strict filtering on all input demons" mentioned above
- "Highest scoring output only" will output the result trees with the highest score (score = skills, recruitable and demon, prioritized in that order)