import os
from scripts.parser import item_parser
from scripts.core import translate, utility

# table header for melee weapons
melee_header = """{| class="wikitable theme-red sortable" style="text-align: center;"
! rowspan=2 | <<icon>>
! rowspan=2 | <<name>>
! rowspan=2 | [[File:Moodle_Icon_HeavyLoad.png|link=|<<weight>>]]
! rowspan=2 | [[File:UI_Hand.png|32px|link=|<<equipped>>]]
! colspan=4 | <<damage>>
! colspan=2 | <<range>>
! rowspan=2 | [[File:UI_AttackSpeed.png|32px|link=|<<attack_speed>>]]
! rowspan=2 | [[File:UI_CriticalHit_Chance.png|32px|32px|link=|<<crit_chance>>]]
! rowspan=2 | [[File:UI_CriticalHit_Multiply.png|32px|link=|<<crit_multiplier>>]]
! rowspan=2 | [[File:UI_Knockback.png|32px|link=|<<knockback>>]]
! rowspan=2 | [[File:UI_Condition_Max.png|32px|link=|<<max_condition>>]]
! rowspan=2 | [[File:UI_Condition_Chance.png|<<condition_lower_chance>>]]
! rowspan=2 | [[File:UI_Condition_Average.png|32px|link=|<<average_condition>>]]
! rowspan=2 | <<item_id>>
|-
! [[File:UI_Damage_Min.png|32px|link=|<<min_damage>>]]
! [[File:UI_Damage_Max.png|32px|link=|<<max_damage>>]]
! [[File:UI_Door.png|32px|link=|<<door_damage>>]]
! rowspan=2 | [[File:Container_Plant.png|32px|link=|<<tree_damage>>]]
! [[File:UI_Range_Min.png|32px|link=|<<min_range>>]]
! style="border-right: var(--border-mw);" | [[File:UI_Range_Max.png|32px|link=|<<max_range>>]]\n"""

# table header for firearms
firearm_header = """{| class="wikitable theme-red sortable" style="text-align: center;"
! rowspan=2 | <<icon>>
! rowspan=2 | <<name>>
! rowspan=2 | [[File:Moodle_Icon_HeavyLoad.png|link=|<<weight>>]]
! rowspan=2 | [[File:UI_Hand.png|32px|link=|<<equipped>>]]
! rowspan=2 | [[File:UI_Ammo.png|link=|<<ammo>>]]
! rowspan=2 | [[File:BerettaClip.png|link=|<<mag_capacity>>]]
! colspan=2 | <<damage>>
! colspan=2 | <<range>>
! rowspan=2 | [[File:UI_Accuracy.png|32px|link=|<<accuracy>>]]
! rowspan=2 | [[File:UI_Accuracy_Add.png|32px|link=|<<accuracy_add>>]]
! rowspan=2 | [[File:UI_CriticalHit_Chance.png|32px|link=|<<crit_chance>>]]
! rowspan=2 | [[File:UI_Critical_Add.png|32px|link=|<<crit_chance_add>>]]
! rowspan=2 | [[File:UI_Noise.png|32px|link=|<<noise_radius>>]]
! rowspan=2 | [[File:UI_Knockback.png|32px|link=|<<knockback>>]]
! rowspan=2 | <<item_id>>
|-
! [[File:UI_Damage_Min.png|32px|link=|<<min_damage>>]]
! [[File:UI_Damage_Max.png|32px|link=|<<max_damage>>]]
! [[File:UI_Range_Min.png|32px|link=|<<min_range>>]]
! style="border-right: var(--border-mw);" | [[File:UI_Range_Max.png|32px|link=|<<max_range>>]]\n"""

# store translated skills
skills = {}


# function to be efficient with translating skills
def translate_skill(skill, property="Categories"):
    if skill not in skills:
        try:
            skill_translated = translate.get_translation(skill, property)
            skills[skill] = skill_translated
        except Exception as e:
            print(f"Error translating skill '{skill}': {e}")
            skill_translated = skill
    else:
        skill_translated = skills[skill]
    return skill_translated


# get values for each firearm
def process_item_firearm(item_data, item_id):
    skill = "Handgun"
    equipped = "1H"
    if item_data.get("RequiresEquippedBothHands", '').lower() == "true":
        skill = "Rifle"
        equipped = "2H"
        if int(item_data.get("ProjectileCount")) > 1:
            skill = "Shotgun"
    
    name = item_data.get('DisplayName', 'Unknown')
    name = translate.get_translation(item_id, 'DisplayName')
    page_name = utility.get_page(item_id)
    link = utility.format_link(name, page_name)
    icon = utility.get_icon(item_data, item_id)
    
    ammo = "-"
    ammo_id = item_data.get('AmmoType', '')
    if ammo_id:
        ammo_data = utility.get_item_data_from_id(ammo_id)
        ammo_name = ammo_data.get('DisplayName', 'Unknown')
        ammo_page = utility.get_page(ammo_id)
        ammo_icon = utility.get_icon(ammo_data, ammo_id)
        ammo = f"[[File:{ammo_icon}.png|link={ammo_page}|{ammo_name}]]"

    condition_max = item_data.get("ConditionMax", '0')
    condition_chance = item_data.get("ConditionLowerChanceOneIn", '0')
    condition_average = str(int(condition_max) * int(condition_chance))

    item = {
        "name": name,
        "icon": f"[[File:{icon}.png|link={page_name}|{name}]]",
        "name_link": link,
        "weight": item_data.get('Weight', '1'),
        "equipped": equipped,
        "ammo": ammo,
        "clip_size": item_data.get('MaxAmmo', item_data.get('ClipSize', '')),
        "damage_min": item_data.get('MinDamage', '-'),
        "damage_max": item_data.get('MaxDamage', '-'),
        "min_range": item_data.get('MinRange', '-'),
        "max_range": item_data.get('MaxRange', '-'),
        "hit_chance": item_data.get('HitChance', '-') + '%',
        "hit_chance_mod": '+' + item_data.get('AimingPerkHitChanceModifier', '-') + '%',
        "crit_chance": item_data.get('CriticalChance', '-') + '%',
        "crit_chance_mod": '+' + item_data.get('AimingPerkCritModifier', '-') + '%',
        "sound_radius": item_data.get('SoundRadius', '-'),
        "knockback": item_data.get('PushBackMod', '-'),
#        "condition_max": condition_max,
#        "condition_chance": condition_chance,
#        "condition_average": condition_average,
        "item_id": f'{{{{ID|{item_id}}}}}',
    }

    return skill, item


# get values for each melee waepon
def process_item_melee(item_data, item_id):
    language_code = translate.get_language_code()
    if language_code == 'en':
        lcs = ""
    else:
        lcs = f"/{language_code}"
    
    skill = item_data.get("Categories", '')
    if isinstance(skill, str):
        skill = [skill]
    # remove "Improvised" from list
    if "Improvised" in skill and len(skill) > 1:
        skill = [cat for cat in skill if cat != "Improvised"]

    skill = " and ".join(skill)
    skill_translated = translate_skill(skill, "Categories")
    if skill_translated is not None:
        skill = skill_translated
    
    name = item_data.get('DisplayName', 'Unknown')
    page_name = utility.get_page(item_id, name)
    name = translate.get_translation(item_id, 'DisplayName')
    link = utility.format_link(name, page_name)
    icon = utility.get_icon(item_data, item_id)

    equipped = "1H"
    if item_data.get("RequiresEquippedBothHands", "FALSE").lower() == "true":
        equipped = "2H"
    elif item_data.get("TwoHandWeapon", "FALSE").lower() == "true":
        equipped = "{{Tooltip|2H*|Limited impact when used one-handed.}}"
    if item_data.get("CloseKillMove") == "Jaw_Stab":
        equipped = "{{Tooltip|1H*|Has jaw stab attack.}}"

    crit_chance = item_data.get("CriticalChance", "-")
    if crit_chance != "-":
        crit_chance = f"{crit_chance}%"
    crit_multiplier = item_data.get("CritDmgMultiplier", "-")
    if crit_multiplier != "-":
        crit_multiplier = f"{crit_multiplier}×"

    condition_max = item_data.get("ConditionMax", '0')
    condition_chance = item_data.get("ConditionLowerChanceOneIn", '0')
    condition_average = str(int(condition_max) * int(condition_chance))

    item = {
        "name": name,
        "icon": f"[[File:{icon}.png|link={page_name}{lcs}|{name}]]",
        "name_link": link,
        "weight": item_data.get('Weight', '1'),
        "equipped": equipped,
        "damage_min": item_data.get('MinDamage', '-'),
        "damage_max": item_data.get('MaxDamage', '-'),
        "damage_door": item_data.get('DoorDamage', '-'),
        "damage_tree": item_data.get('TreeDamage', '-'),
        "min_range": item_data.get('MinRange', '-'),
        "max_range": item_data.get('MaxRange', '-'),
        "base_speed": item_data.get('BaseSpeed', '1'),
        "crit_chance": crit_chance,
        "crit_multiplier": crit_multiplier,
        "knockback": item_data.get('PushBackMod', '-'),
        "condition_max": condition_max,
        "condition_chance": condition_chance,
        "condition_average": condition_average,
        "item_id": f"{{{{ID|{item_id}}}}}",
    }

    return skill, item


# write to file
def write_items_to_file(skills, header, category):
    language_code = translate.get_language_code()
    output_dir = f'output/{language_code.upper()}/item_list/weapons/{category}/'
    os.makedirs(output_dir, exist_ok=True)
    
    for skill, items in skills.items():
        output_path = f"{output_dir}{skill}.txt"
        with open(output_path, 'w', encoding='utf-8') as file:
            header = translate.get_wiki_translation(header)
            file.write(f"{header}")
            sorted_items = sorted(items, key=lambda x: x['name'])

            for item in sorted_items:
                # remove 'name' before writing
                item = [value for key, value in item.items() if key != 'name']
                item = '\n| '.join(item)
                file.write(f"|-\n| {item}\n")
            file.write("|}")


def get_items():
    melee_skills = {}
    firearm_skills = {}

    for item_id, item_data in item_parser.get_item_data().items():
        if item_data.get("Type") == "Weapon":

            if item_data.get("Categories"):
                skill, item = process_item_melee(item_data, item_id)

                if skill not in melee_skills:
                    melee_skills[skill] = []
                melee_skills[skill].append(item)

            elif item_data.get("SubCategory") == "Firearm":
                skill, item = process_item_firearm(item_data, item_id)

                if skill not in firearm_skills:
                    firearm_skills[skill] = []
                firearm_skills[skill].append(item)

            # TODO: add explosives

    write_items_to_file(melee_skills, melee_header, 'melee')
    write_items_to_file(firearm_skills, firearm_header, 'firearm')


def main():
    get_items()


if __name__ == "__main__":
    main()
