from copy import deepcopy
from dataclasses import dataclass
from typing import Union

from Basics import getPratyahara, getBaseSvara, getSavarnas, getSvaraVariations, doPadaVigraha, doVarnaMelana, d_abhyatnamap, d_bahyatnamap, d_sthanamap
from Main import Padam
from Samjna import isHrsva, isAnunasika, isSavarna, getGunas, getVriddhis, isDeergha, isPluta, isPragruhya
from Utilities import flatten_and_set

@dataclass
class SutraAction:
    SutraNum: str
    Lakshyam: int
    Vishaya: str
    Type: str
    Expr: list


class SandhiPrakriya:
    def __init__(self, first_exp=None):
        self.first_exp = first_exp
        self.l_prakriya = []

    @property
    def l_exps(self):
        return [self.first_exp] + [i.Expr for i in self.l_prakriya]

    @property
    def l_sutrams(self):
        return [i.SutraNum for i in self.l_prakriya]

    @property
    def l_lak_sutrams(self):
        return [(i.Lakshyam, i.SutraNum) for i in self.l_prakriya]

    @property
    def l_lak_vis_types(self):
        return [(i.Lakshyam, i.Vishaya, i.Type) for i in self.l_prakriya]

    def get_all_actions(self, *args: str):
        return [[getattr(act, col) for col in args] for act in self.l_prakriya]

    def add_entry(self, sutram, lakshyam, vishaya, actiontype, expr):
        self.l_prakriya.append(SutraAction(sutram, lakshyam, vishaya, actiontype, expr))
        # self.l_prakriya.append({"Sutram": sutram, "Lakshyam": lakshyam, "Action": action, "ActionType": actiontype, "Exp": expr})

    def edit_entry(self, new_set, ind=None, row_set=None):
        if ind:
            self.l_prakriya[ind] = SutraAction(new_set[0], new_set[1], new_set[2], new_set[3], new_set[4])
            # self.l_prakriya[ind] = {"Sutram": new_set[0], "Lakshyam": new_set[1], "Action": new_set[2], "ActionType": new_set[3], "Exp": new_set[4]}
        elif row_set:
            pass

    def fork_new_with_entry(self, sutram, lakshyam, action, actiontype, expr):
        new_p = deepcopy(self)
        new_p.add_entry(sutram, lakshyam, action, actiontype, expr)
        return new_p


def getValidRoopa(allnums, allexps, thisnum):
    allnums = list(allnums)
    if allnums:
        exp_sets = dict(zip(allnums, allexps[1:]))
        removevals = []
        for i in range(len(allnums)):
            if allnums[i] > thisnum and allnums[i] > '8.2.0':
                removevals.append(allnums[i])
        if removevals:
            for val in removevals:
                allnums.remove(val)

            if allnums:
                return exp_sets[allnums[-1]]
            else:
                return allexps[0]
    return allexps[-1]

def hasSiddhaAhead(lexp1, lexp2, ind, c_sutram, no_vikalpa, prakriya):
    if ind == len(lexp1) - 1 or (ind == len(lexp2) - 1 and ind > len(lexp1) - 1):
        return False
    l_check = list(lexp1) + lexp2[:2] if ind < len(lexp1) - 1 else list(lexp2)
    padanta = len(l_check) - 3 if ind < len(lexp1) - 1 and lexp2 else len(l_check) - 1
    endpoint = padanta + 1 if ind < len(lexp1) - 1 and lexp2 else padanta
    newind = ind if ind < len(lexp1) - 1 and lexp2 else ind - len(lexp1)
    # print('--', l_check, padanta, endpoint)
    for i in range(newind + 1, endpoint):
        # print('--', l_check[i - 1], l_check[i], l_check[i + 1])
        orgind = i if ind < len(lexp1) - 1 and lexp2 else i + len(lexp1)
        # ?????????????????????????????? ??????????????????????????? ???????????????????????????
        if i == padanta and l_check[i] in getPratyahara('?????????') and l_check[i + 1] in getPratyahara('?????????') and l_check[i + 1] and not isSavarna(l_check[i], l_check[i + 1]) and (orgind, '6.1.127') not in prakriya.l_lak_sutrams and '6.1.127' < c_sutram and not no_vikalpa:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.127')
            if l_rightexp == lexp1 + lexp2:
                return True

        # ??????????????????
        if i == padanta and l_check[i] in getPratyahara('?????????') and l_check[i + 1] in getPratyahara('?????????') and (orgind, '6.1.128') not in prakriya.l_lak_sutrams and '6.1.128' < c_sutram and not no_vikalpa:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.128')
            if l_rightexp == lexp1 + lexp2:
                return True

        # ????????? ????????????
        if l_check[i] in getPratyahara('?????????') and l_check[i + 1] in getPratyahara('?????????') and l_check[i + 1] not in getSavarnas(getBaseSvara(l_check[i])) and (orgind, '6.1.77') not in prakriya.l_lak_sutrams and '6.1.77' < c_sutram:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.77')
            if l_rightexp == lexp1 + lexp2:
                return True

        # ????????? ??????????????????????????????
        if i == padanta and l_check[i] in getPratyahara('?????????') and l_check[i + 1][0] in getSavarnas('???') and ((orgind, orgind + 1), '6.1.109') not in prakriya.l_lak_sutrams and '6.1.109' < c_sutram:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.109')
            if l_rightexp == lexp1 + lexp2:
                return True

        # ?????????????????????????????????
        if l_check[i] in getPratyahara('?????????') and l_check[i + 1] in getPratyahara('?????????') and (orgind, '6.1.78') not in prakriya.l_lak_sutrams and '6.1.78' < c_sutram:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.78')
            if l_rightexp == lexp1 + lexp2:
                return True

        # ??????????????????????????????
        if l_check[i] in getSavarnas('???')  and l_check[i + 1] in getPratyahara('?????????') and ((orgind, orgind + 1), '6.1.88') not in prakriya.l_lak_sutrams and '6.1.88' < c_sutram:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.88')
            if l_rightexp == lexp1 + lexp2:
                return True

        # ????????? ?????????????????? ??????????????????
        if l_check[i] in getPratyahara('?????????') and l_check[i + 1] in getSavarnas(l_check[i][0]) and ((orgind, orgind + 1), '6.1.101') not in prakriya.l_lak_sutrams and '6.1.101' < c_sutram:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.101')
            if l_rightexp == lexp1 + lexp2:
                return True

        # ?????????????????????
        if l_check[i] in getSavarnas('???') and l_check[i + 1] in getPratyahara('?????????') and ((orgind, orgind + 1), '6.1.87') not in prakriya.l_lak_sutrams and '6.1.87' < c_sutram:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.87')
            if l_rightexp == lexp1 + lexp2:
                return True

        # ?????? ???
        if isHrsva(l_check[i]) and l_check[i + 1] == '??????' and (orgind, '6.1.73') not in prakriya.l_lak_sutrams and '6.1.73' < c_sutram:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.73')
            if l_rightexp == lexp1 + lexp2:
                return True

        # ?????????????????????????????????
        if i == padanta and isDeergha(l_check[i]) and l_check[i + 1] == '??????' and not no_vikalpa and (orgind, '6.1.76') not in prakriya.l_lak_sutrams and '6.1.76' < c_sutram:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.76')
            if l_rightexp == lexp1 + lexp2:
                return True

        # ????????? ????????????????????????????????????????????????, ????????? ???
        if i + 1 == padanta and doVarnaMelana(l_check[i: i + 2]) == '?????????' and l_check[i - 1] in getPratyahara('?????????') and (l_check[i + 2] in getPratyahara('?????????') or l_check[i + 2] in getPratyahara('?????????')) and (orgind, '6.1.113') not in prakriya.l_lak_sutrams and '6.1.113' < c_sutram:
            l_rightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '6.1.113')
            if (i, '?????????', 'Adesha') in prakriya.l_lak_vis_types or l_rightexp == lexp1 + lexp2:
                return True

        # ???????????????????????????????????? ????????????
        if i == padanta and (l_check[i] in getPratyahara('?????????') and l_check[i - 1] in getPratyahara('?????????')) and i != 0 and l_check[i] not in getPratyahara('?????????') and (orgind, '8.2.23') not in prakriya.l_lak_sutrams and '8.2.23' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.2.23')
            if lrightexp == lexp1 + lexp2:
                return True

        # ????????? ?????????
        if l_check[i] in getPratyahara('??????') and (i == padanta or l_check[i + 1] in getPratyahara('?????????')) and (orgind, '8.2.30') not in prakriya.l_lak_sutrams and '8.2.30' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.2.30')
            if lrightexp == lexp1 + lexp2:
                return True

        # ???????????? ????????????????????????
        if i == padanta and l_check[i] in getPratyahara('?????????') and (orgind, '8.2.39') not in prakriya.l_lak_sutrams and '8.2.39' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.2.39')
            if lrightexp == lexp1 + lexp2:
                return True

        # ?????????????????? ?????????
        if i == padanta and l_check[i] == '??????' and (orgind, '8.2.66') not in prakriya.l_lak_sutrams and '8.2.66' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.2.66')
            if lrightexp == lexp1 + lexp2:
                return True

        # ??????????????????????????????????????????
        if i == padanta and l_check[i] == '??????' and l_check[i + 1] in getPratyahara('?????????') and l_check[i + 2] in getPratyahara('?????????') and (orgind, '8.3.07') not in prakriya.l_lak_sutrams and '8.3.07' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.07')
            if lrightexp == lexp1 + lexp2:
                return True

        # ?????? ?????? ????????????
        if i == padanta and l_check[i] == '??????' and l_check[i + 1] == '??????' and (orgind, '8.3.13') not in prakriya.l_lak_sutrams and '8.3.13' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.13')
            if lrightexp == lexp1 + lexp2:
                return True

        # ?????? ??????
        if i == padanta and l_check[i] == '??????' and l_check[i + 1] == '??????' and (orgind, '8.3.14') not in prakriya.l_lak_sutrams and '8.3.14' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.14')
            if lrightexp == lexp1 + lexp2:
                return True

        # ??????????????????????????? ??????????????????????????????
        if i == padanta and l_check[i] == '??????' and l_check[i + 1] in getPratyahara('?????????') and (orgind, '8.3.15') not in prakriya.l_lak_sutrams and '8.3.15' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.15')
            if lrightexp == lexp1 + lexp2:
                return True

        # ??????????????????????????????????????????????????? ???????????????
        if i + 1 == padanta and doVarnaMelana(l_check[i: i + 2]) == '?????????' and l_check[i - 1] in getSavarnas('???') and i != 0 and l_check[i + 2] in getPratyahara('?????????') and (orgind, '8.3.17') not in prakriya.l_lak_sutrams and '8.3.17' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.17')
            if lrightexp == lexp1 + lexp2:
                return True

        # ???????????? ???????????????????????????
        if i == padanta and (l_check[i] in ['??????', '??????'] and l_check[i + 1] in getPratyahara('?????????')) and l_check[i - 1][0] in getSavarnas('???') and i != 0 and not no_vikalpa and (orgind, '8.3.19') not in prakriya.l_lak_sutrams and '8.3.19' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.19')
            if lrightexp == lexp1 + lexp2:
                return True

        # ????????? ???????????????????????????
        if i == padanta and l_check[i] == '??????' and l_check[i + 1] in getPratyahara('?????????') and (orgind, '8.3.22') not in prakriya.l_lak_sutrams and '8.3.22' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.22')
            if lrightexp == lexp1 + lexp2:
                return True

        # ?????????????????????????????????
        if i == padanta and l_check[i] == '??????' and l_check[i + 1] in getPratyahara('?????????') + ('??????',) and (orgind, '8.3.23') not in prakriya.l_lak_sutrams and '8.3.23' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.23')
            if lrightexp == lexp1 + lexp2:
                return True

        # ?????????????????????????????????????????? ?????????
        if i != padanta and l_check[i] in ['??????', '??????'] and l_check[i + 1] in getPratyahara('?????????') and (orgind, '8.3.24') not in prakriya.l_lak_sutrams and '8.3.24' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.24')
            if lrightexp == lexp1 + lexp2:
                return True

        # ?????? ???????????? ??????
        if i == padanta and ord(l_check[i][0]) == 2306 and l_check[i + 1] == '??????' and l_check[i + 2] in ['??????', '??????', '??????', '??????'] and not no_vikalpa and (orgind, '8.3.26') not in prakriya.l_lak_sutrams and '8.3.26' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.26')
            if lrightexp == lexp1 + lexp2:
                return True

        # ???????????? ??????
        if i == padanta and ord(l_check[i][0]) == 2306 and l_check[i + 1] == '??????' and l_check[i + 2] == '??????' and not no_vikalpa and (orgind, '8.3.27') not in prakriya.l_lak_sutrams and '8.3.27' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.27')
            if lrightexp == lexp1 + lexp2:
                return True

        # ??????????????? ???????????????????????? ?????????
        if i == padanta and l_check[i] in ['??????', '??????'] and l_check[i + 1] in getPratyahara('?????????') and not no_vikalpa and (orgind, '8.3.28') not in prakriya.l_lak_sutrams and '8.3.28' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.28')
            if lrightexp == lexp1 + lexp2:
                return True

        # ?????? ?????? ????????????, ????????????
        if i == padanta and l_check[i] in ['??????', '??????'] and l_check[i + 1] == '??????' and not no_vikalpa and ((l_check[i] == '??????' and (orgind, '8.3.29') not in prakriya.l_lak_sutrams and '8.3.29' < c_sutram) or (l_check[i] == '??????' and (orgind, '8.3.30') not in prakriya.l_lak_sutrams and '8.3.30' < c_sutram)):
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.29')
            if lrightexp == lexp1 + lexp2:
                return True

        # ?????? ????????????
        if i == padanta and l_check[i] == '??????' and l_check[i + 1] == '??????' and not no_vikalpa and (orgind, '8.3.30') not in prakriya.l_lak_sutrams and '8.3.30' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.30')
            if lrightexp == lexp1 + lexp2:
                return True

        # ????????? ?????????????????????????????? ????????????????????????????????????
        if i == padanta and isHrsva(l_check[i - 1]) and l_check[i] in getPratyahara('?????????') and l_check[i + 1] in getPratyahara('?????????') and (orgind, '8.3.32') not in prakriya.l_lak_sutrams and '8.3.32' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.32')
            if lrightexp == lexp1 + lexp2:
                return True

        # ???????????????????????????????????? ??????
        if i == padanta and l_check[i] == chr(2307) and l_check[i + 1] in getPratyahara('?????????') and (orgind, '8.3.34') not in prakriya.l_lak_sutrams and '8.3.34' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.3.34')
            if lrightexp == lexp1 + lexp2:
                return True

        # ??????????????? ?????????????????? ???????????????
        if (l_check[i] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_check[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????']) or (l_check[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_check[i] in ['??????', '??????', '??????', '??????', '??????', '??????']) and (orgind, '8.4.40') not in prakriya.l_lak_sutrams and '8.4.40' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.40')
            if lrightexp == lexp1 + lexp2:
                return True

        # ?????????????????? ???????????????
        if (l_check[i] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_check[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????']) or (l_check[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_check[i] in ['??????', '??????', '??????', '??????', '??????', '??????']) and (orgind, '8.4.41') not in prakriya.l_lak_sutrams and '8.4.41' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.41')
            if lrightexp == lexp1 + lexp2:
                return True

        # ???????????????????????????????????? ??????????????????????????? ??????
        if i == padanta and l_check[i] in getPratyahara('?????????') and getSavarnas(l_check[i]) and l_check[i + 1] in ['??????', '??????', '??????', '??????', '??????', '?????????', '?????????', '?????????'] and (orgind, '8.4.45') not in prakriya.l_lak_sutrams and '8.4.45' < c_sutram and not no_vikalpa:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.45')
            if lrightexp == lexp1 + lexp2:
                return True

        # ????????? ???????????????????????? ????????????
        if i != padanta and l_check[i - 2] in getPratyahara('?????????') + (chr(2306), ) and l_check[i - 1] in ['??????', '??????'] and i >= 2 and l_check[i] in getPratyahara('?????????') and not no_vikalpa and (orgind, '8.4.46') not in prakriya.l_lak_sutrams and '8.4.46' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.46')
            if lrightexp == lexp1 + lexp2:
                return True

        # ???????????? ???
        if l_check[i - 1] in getPratyahara('?????????') + (chr(2306), ) and i != 0 and l_check[i] in getPratyahara('?????????') and l_check[i + 1] not in getPratyahara('?????????') and not no_vikalpa and (orgind, '8.4.47') not in prakriya.l_lak_sutrams and '8.4.47' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.47')
            if lrightexp == lexp1 + lexp2:
                return True

        # ???????????? ????????? ?????????
        if l_check[i] in getPratyahara('?????????') and l_check[i + 1] in getPratyahara('?????????') and (orgind, '8.4.53') not in prakriya.l_lak_sutrams and '8.4.53' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.53')
            if lrightexp == lexp1 + lexp2:
                return True

        # ????????? ???
        if l_check[i] in getPratyahara('?????????') and l_check[i + 1] in getPratyahara('?????????') and (orgind, '8.4.55') not in prakriya.l_lak_sutrams and '8.4.55' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.55')
            if lrightexp == lexp1 + lexp2:
                return True

        # ????????????????????????????????? ????????? ????????????????????????,  ?????? ???????????????????????????
        if ord(l_check[i][0]) == 2306 and l_check[i + 1] in getPratyahara('?????????') and ((i != padanta and (orgind, '8.4.58') not in prakriya.l_lak_sutrams and '8.4.58' < c_sutram) or (i == padanta and (orgind, '8.4.59') not in prakriya.l_lak_sutrams and '8.4.59' < c_sutram and not no_vikalpa)):
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.58')
            if lrightexp == lexp1 + lexp2:
                return True

        # ??????????????????
        if l_check[i] in getPratyahara('??????') and l_check[i + 1] == '??????' and (orgind, '8.4.60') not in prakriya.l_lak_sutrams and '8.4.60' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.60')
            if lrightexp == lexp1 + lexp2:
                return True

        # ????????? ??????????????????????????????????????????
        if l_check[i - 1] in getPratyahara('?????????') and i != 0 and l_check[i] == '??????' and (orgind, '8.4.62') not in prakriya.l_lak_sutrams and '8.4.62' < c_sutram and not no_vikalpa:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.62')
            if lrightexp == lexp1 + lexp2:
                return True

        # ????????????????????????
        if l_check[i - 1] in getPratyahara('?????????') and i != 0 and l_check[i] == '??????' and l_check[i + 1] in getPratyahara('?????????') and (orgind, '8.4.63') not in prakriya.l_lak_sutrams and '8.4.63' < c_sutram and not no_vikalpa:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.63')
            if lrightexp == lexp1 + lexp2:
                return True

        # ????????? ????????? ??????????????????
        if l_check[i] in getPratyahara('?????????') and l_check[i + 1] in getPratyahara('?????????') and l_check[i + 1] in getSavarnas(l_check[i]) and l_check[i - 1] in getPratyahara('?????????') and i != 0 and not no_vikalpa and (orgind, '8.4.65') not in prakriya.l_lak_sutrams and '8.4.65' < c_sutram:
            lrightexp = getValidRoopa(prakriya.l_sutrams, prakriya.l_exps, '8.4.65')
            if lrightexp == lexp1 + lexp2:
                return True

        # # ????????????????????????????????????????????? ?????????
        # if i + 1 == padanta and doVarnaMelana(l_check[i: i + 2]) == '?????????' and (i, '?????????', 'Adesha') in prakriya.l_lak_vis_types and '1.3.09' < c_sutram:
        #     return True

    else:
        return False

def getAdeshaBySthana(sthani, adesha):  # Based on ?????????????????????????????????????????? (1.1.50)
    """
    @param sthani: List of sthanis. Mostly contains one letter. Sometimes two sthanis
    @param adesha: Adesha
    """
    sthani[0] = getBaseSvara(sthani[0]) if sthani[0] in getPratyahara('?????????') else sthani[0][:2]
    if len(sthani) == 1:
        st_sthana = d_sthanamap[sthani[0]]
    else:
        sthani[1] = getBaseSvara(sthani[1]) if sthani[1] in getPratyahara('?????????') else sthani[1][:2]
        if d_sthanamap[sthani[0]] in d_sthanamap[sthani[1]]:
            st_sthana = d_sthanamap[sthani[1]]
        elif d_sthanamap[sthani[1]] in d_sthanamap[sthani[0]]:
            st_sthana = d_sthanamap[sthani[0]]
        else:
            st_sthana = d_sthanamap[sthani[0]] + d_sthanamap[sthani[1]]

    l_adeshas = list(getPratyahara(adesha, withSavarnas=False)) if isinstance(adesha, str) else adesha[:]
    l_adsthanas, l_candids = [], []
    for ad in l_adeshas:
        if ad in getPratyahara('?????????'):
            ad_sthana = d_sthanamap[getBaseSvara(ad)] + ' and Nasika' if isAnunasika(ad) else d_sthanamap[getBaseSvara(ad)]
        else:
            ad_sthana = d_sthanamap[ad[:2]] + ' and Nasika' if isAnunasika(ad) and ' and Nasika' not in d_sthanamap[ad[:2]] else d_sthanamap[ad]
        l_adsthanas.append(ad_sthana)
    for i in range(len(l_adsthanas)):
        if l_adsthanas[i] == st_sthana:
            l_candids.append(l_adeshas[i])
    if len(l_candids) == 0:
        for i in range(len(l_adsthanas)):
            if (l_adsthanas[i] in st_sthana and " " not in st_sthana) or (st_sthana in l_adsthanas[i] and " " not in l_adsthanas[i]) or ('Nasika' in st_sthana and 'Nasika' in l_adsthanas[i]):
                l_candids.append(l_adeshas[i])
    if len(l_candids) == 1:
        return l_candids[0]
    else:
        # Abhyantara check
        l_candids = list(l_adeshas) if not l_candids else l_candids
        l_adabhs, l_candids_abh = [d_abhyatnamap[getBaseSvara(ad)] if ad in getPratyahara('?????????') else d_abhyatnamap[ad[:2]] for ad in l_candids], []
        for j in range(len(l_adabhs)):
            if l_adabhs[j] == d_abhyatnamap[sthani[0]]:
                l_candids_abh.append(l_candids[j])
        if len(l_candids_abh) == 1:
            return l_candids_abh[0]
        else:
            # Bahya check
            l_adbahs, l_candids_bah = [d_bahyatnamap[getBaseSvara(ad)] if ad in getPratyahara('?????????') else d_bahyatnamap[ad[:2]] for ad in l_candids], []
            for k in range(len(l_adbahs)):
                if l_adbahs[k] == d_bahyatnamap[sthani[0]]:
                    l_candids_bah.append(l_candids[k])

            if len(l_candids_bah) == 1:
                return l_candids_bah[0]

def doSandhi(expr1: Union[str, list, tuple, Padam], expr2: Union[str, list, tuple, Padam] = '', at_padanta=True, no_vikalpa=True, prakriya: SandhiPrakriya = None) -> str:
    """
    @param expr1: First expression
    @param expr2: Second expression
    @param at_padanta: If true, the first expression is taken as a Padam
    @param no_vikalpa: If true, Return only paninian roopams
    @param prakriya: SandhiPrakriya object which tracks all changes like sutrams, lakshyams, actions, actiontypes, and resulting expresions
    """

    if not expr2:
        l_exp = doPadaVigraha(expr1) if isinstance(expr1, (str, Padam)) else list(expr1)
        l_exp1, l_exp2 = list(l_exp), []
    else:
        if isinstance(expr1, (str, Padam)):
            l_exp1 = doPadaVigraha(expr1)
        else:
            l_exp1 = list(expr1)
        if isinstance(expr2, (str, Padam)):
            l_exp2 = doPadaVigraha(expr2)
        else:
            l_exp2 = list(expr2)
        l_exp = l_exp1 + l_exp2
    padanta = len(l_exp1) - 1 if at_padanta else None
    # if not padanta and not l_exp2:
    #     raise ValueError("Pass as two elements when the whole word is not a padam")

    prak_set = prakriya
    if not prakriya:
        prak_set = SandhiPrakriya(first_exp=list(l_exp))
    print(l_exp, padanta)
    print(prak_set.l_lak_sutrams)
    print(prak_set.l_lak_vis_types)
    for i in range(len(l_exp) - 1):
        print(l_exp[i - 1], l_exp[i], l_exp[i + 1])

        # ??????????????????
        if i == padanta and l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getPratyahara('?????????') and (i, '6.1.128') not in prak_set.l_lak_sutrams and not no_vikalpa:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.128')
            if l_rightexp == l_exp:
                v_pset = prak_set.fork_new_with_entry('6.1.128', i, None, 'AdeshaPrakrutiVikalpa', list(l_exp))
                prak_set.add_entry('6.1.128', i, l_exp[i], 'AdeshaPrakrutibhava', l_exp)

                # res1 = doSandhi(l_exp[:i + 1], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                # res2 = doSandhi(l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                # if isinstance(res1, tuple) and isinstance(res2, tuple):
                #     result = tuple([j + k for j in flatten_and_set(res1) for k in flatten_and_set(res2)])
                # elif isinstance(res1, str) and isinstance(res2, tuple):
                #     result = tuple([res1 + j for j in flatten_and_set(res2)])
                # elif isinstance(res2, str) and isinstance(res1, tuple):
                #     result = tuple([j + res2 for j in flatten_and_set(res1)])
                # else:
                #     result = res1 + res2

                return doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ?????????????????????????????? ??????????????????????????? ???????????????????????????
        if i == padanta and l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getPratyahara('?????????') and l_exp[i + 1] and not isSavarna(l_exp[i], l_exp[i + 1]) and (i, '6.1.127') not in prak_set.l_lak_sutrams and not no_vikalpa:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.127')
            if l_rightexp == l_exp:
                v_pset = prak_set.fork_new_with_entry('6.1.127', i, None, 'AdeshaPrakrutiVikalpa', list(l_exp))
                if isDeergha(l_exp[i]):
                    l_exp[i] = getSvaraVariations(getBaseSvara(l_exp[i]), 'Hrsva')[0]
                prak_set.add_entry('6.1.127', i, l_exp[i], 'AdeshaPrakrutibhava', l_exp)

                return doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ?????????????????????????????????????????? ????????? ?????????????????????
        if (isPluta(l_exp[i]) or isPragruhya(doVarnaMelana(l_exp1))) and l_exp[i + 1] in getPratyahara('?????????') and (i, '6.1.125') not in prak_set.l_lak_sutrams:
            prak_set.add_entry('6.1.125', i, l_exp[i], 'Prakrutibhava', l_exp)

            return doSandhi(l_exp1[:i + 1], l_exp2[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ????????? ????????????
        if l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getPratyahara('?????????') and l_exp[i + 1] not in getSavarnas(getBaseSvara(l_exp[i])) and (i, '6.1.77') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.77')
            if l_rightexp == l_exp and not any(i == j[0] and 'Prakrutibhava' in j[2] for j in prak_set.l_lak_vis_types):
                l_exp[i] = getAdeshaBySthana([l_exp[i]], '?????????')
                prak_set.add_entry('6.1.77', i, l_exp[i], 'Adesha', l_exp)

                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ????????? ??????????????????????????????
        if i == padanta and l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getPratyahara('?????????') and ((i, i + 1), '6.1.109') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.109')
            if l_rightexp == l_exp and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                prak_set.add_entry('6.1.109', (i, i + 1), l_exp[i], 'Adesha', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 2:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ?????????????????????????????????
        if l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getPratyahara('?????????') and (i, '6.1.78') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.78')
            if l_rightexp == l_exp and not any(i == j[0] and 'Prakrutibhava' in j[2] for j in prak_set.l_lak_vis_types) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                adesha = doPadaVigraha({'???': '?????????', '???': '?????????', '???': '?????????', '???': '?????????'}[getBaseSvara(l_exp[i])])
                l_exp = l_exp[:i] + adesha + l_exp[i + 1:]
                prak_set.add_entry('6.1.78', i, adesha, 'Adesha', l_exp)

                padanta = padanta + 1 if padanta and i <= padanta else padanta
                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ??????????????????????????????
        if l_exp[i] in getSavarnas('???') and l_exp[i + 1] in getPratyahara('?????????') and ((i, i + 1), '6.1.88') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.88')
            if l_rightexp == l_exp and not any(i == j[0] and 'Prakrutibhava' in j[2] for j in prak_set.l_lak_vis_types) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                adesha = [getAdeshaBySthana(['???', l_exp[i + 1]], getVriddhis(False))]
                if adesha == ['???'] and l_exp[i + 1] in ['???', '???']:
                    adesha.append(getAdeshaBySthana(l_exp[i + 1], '???'))  # ???????????? ???????????? (1.1.51)
                l_exp = l_exp[:i] + adesha + l_exp[i + 2:]
                prak_set.add_entry('6.1.88', (i, i + 1), adesha, 'Adesha', l_exp)

                if padanta and i != padanta:
                    padanta = padanta - 1 if i < padanta and len(adesha) == 1 else padanta
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    if len(adesha) == 1:
                        return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                    else:
                        return doSandhi(l_exp[:i], l_exp[i:], at_padanta=False, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ????????? ?????????????????? ??????????????????
        if l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getSavarnas(l_exp[i][0]) and ((i, i + 1), '6.1.101') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.101')
            if l_rightexp == l_exp and not any(i == j[0] and 'Prakrutibhava' in j[2] for j in prak_set.l_lak_vis_types) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                adesha = [getSvaraVariations(getBaseSvara(l_exp[i]), 'Deergha')[0]]
                l_exp = l_exp[:i] + adesha + l_exp[i + 2:]
                prak_set.add_entry('6.1.101', (i, i + 1), adesha, 'Adesha', l_exp)
                if padanta and i != padanta:
                    padanta = padanta - 1 if i < padanta else padanta
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ?????????????????????
        if l_exp[i] in getSavarnas('???') and l_exp[i + 1] in getPratyahara('?????????') and ((i, i + 1), '6.1.87') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.87')
            if l_rightexp == l_exp and not any(i == j[0] and 'Prakrutibhava' in j[2] for j in prak_set.l_lak_vis_types) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                adesha = [getAdeshaBySthana(['???', l_exp[i + 1]], getGunas(False))]
                if adesha == ['???'] and l_exp[i + 1] in ['???', '???']:
                    adesha.append(getAdeshaBySthana([l_exp[i + 1]], '???'))  # ???????????? ???????????? (1.1.51)
                l_exp = l_exp[:i] + adesha + l_exp[i + 2:]
                prak_set.add_entry('6.1.87', (i, i + 1), adesha, 'Adesha', l_exp)

                if padanta and i != padanta:
                    padanta = padanta - 1 if i < padanta and len(adesha) == 1 else padanta
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    if len(adesha) == 1:
                        return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                    else:
                        return doSandhi(l_exp[:i], l_exp[i:], at_padanta=False, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ?????? ???
        if isHrsva(l_exp[i]) and l_exp[i + 1] == '??????' and (i, '6.1.73') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.73')
            if l_rightexp == l_exp and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp.insert(i + 1, '??????')
                prak_set.add_entry('6.1.73', i, '????????????', 'Agama', l_exp)

                if padanta and i != padanta:
                    padanta = padanta + 1 if i < padanta else padanta
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 2], l_exp[i + 2:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ????????????????????????, ?????????????????????????????????
        if isDeergha(l_exp[i]) and l_exp[i + 1] == '??????' and ((i != padanta and (i, '6.1.75') not in prak_set.l_lak_sutrams) or (i == padanta and (i, '6.1.76') not in prak_set.l_lak_sutrams and not no_vikalpa)):
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.75')
            if l_rightexp == l_exp and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp.insert(i + 1, '??????')

                if i == padanta and not no_vikalpa:
                    v_pset = prak_set.fork_new_with_entry('6.1.76', i, None, 'AgamaVikalpa', l_exp[:i + 1] + l_exp[i + 2:])
                    prak_set.add_entry('6.1.76', i, '????????????', 'Agama', l_exp)
                    return doSandhi(l_exp[:i + 2], l_exp[i + 2:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)
                prak_set.add_entry('6.1.75', i, '????????????', 'Agama', l_exp)
                if padanta:
                    padanta = padanta + 1 if i < padanta else padanta
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                return doSandhi(l_exp[:i + 2], l_exp[i + 2:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ????????? ????????????????????????????????????????????????, ????????? ???
        if i + 1 == padanta and doVarnaMelana(l_exp[i: i + 2]) == '?????????' and l_exp[i - 1] in getPratyahara('?????????') and (l_exp[i + 2] in getPratyahara('?????????') or l_exp[i + 2] in getPratyahara('?????????')) and (i, '6.1.113') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '6.1.113')
            if (i, '?????????', 'Adesha') in prak_set.l_lak_vis_types or (l_rightexp == l_exp and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam)):
                l_exp[i] = '???'
                l_exp.pop(i + 1)
                if l_exp[i + 1] in getPratyahara('?????????'):
                    prak_set.add_entry('6.1.113', i, l_exp[i], 'Adesha', l_exp)
                else:
                    prak_set.add_entry('6.1.114', i, l_exp[i], 'Adesha', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ???????????????????????????????????? ????????????
        if i == padanta and (l_exp[i] in getPratyahara('?????????') and l_exp[i - 1] in getPratyahara('?????????')) and i != 0 and l_exp[i] not in getPratyahara('?????????') and (i, '8.2.23') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.2.23')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.2.23', no_vikalpa, prak_set) and 'Agama' not in prak_set.get_all_actions('Type') and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                lupta = l_exp.pop(i)
                prak_set.add_entry('8.2.23', i, lupta, 'Lopa', l_exp)

                return doSandhi(l_exp[:i], l_exp[i:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ????????? ?????????
        if l_exp[i] in getPratyahara('??????') and (i == padanta or l_exp[i + 1] in getPratyahara('?????????')) and (i, '8.2.30') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.2.30')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.2.30', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = getPratyahara('??????')[getPratyahara('??????').index(l_exp[i])]
                prak_set.add_entry('8.2.30', i, l_exp[i], 'Adesha', l_exp)

                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ???????????? ????????????????????????
        if i == padanta and l_exp[i] in getPratyahara('?????????') and l_exp[i] not in ['??????', '??????', '??????'] and (i, '8.2.39') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.2.39')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.2.39', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = getAdeshaBySthana([l_exp[i]], '?????????')
                prak_set.add_entry('8.2.39', i, l_exp[i], 'Adesha', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ?????????????????? ?????????  --
        if i == padanta and l_exp[i] == '??????' and (i, '8.2.66') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.2.66')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.2.66', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = '??????'
                l_exp.insert(i + 1, '??????')
                prak_set.add_entry('8.2.66', i, '?????????', 'Adesha', l_exp)

                return doSandhi(l_exp[:i + 2], l_exp[i + 2:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ??????????????????????????????????????????  --
        if i == padanta and l_exp[i] == '??????' and l_exp[i + 1] in getPratyahara('?????????') and l_exp[i + 2] in getPratyahara('?????????') and (i, '8.3.07') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.07')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.07', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] =  '??????'
                l_exp.insert(i + 1, '??????')
                prak_set.add_entry('8.3.07', i, '?????????', 'Adesha', l_exp)

                new_lexp, new_pset = list(l_exp), deepcopy(prak_set)

                l_exp[i - 1] = l_exp[i - 1] + chr(2305)  # ??????????????????????????????????????? ???????????????????????? ?????? ??????
                prak_set.add_entry('8.3.02', i - 1, l_exp[i - 1], 'Adesha', l_exp)

                new_lexp.insert(i, chr(2306))  # ?????????????????????????????????????????????????????????????????????
                new_pset.add_entry('8.3.04', i - 1, chr(2306), 'Agama', new_lexp)
                new_pset.edit_entry(('8.3.07', i + 1, '?????????', 'Adesha', new_lexp), -2)

                return doSandhi(l_exp[:i + 2], l_exp[i + 2:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(new_lexp[:i + 3], new_lexp[i + 3:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=new_pset)

        # ?????? ?????? ????????????
        if i == padanta and l_exp[i] == '??????' and l_exp[i + 1] == '??????' and (i, '8.3.13') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.13')
            if (l_rightexp == l_exp or (i + 1, '8.4.41') in prak_set.l_lak_sutrams) and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.13', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                lupta = l_exp.pop(i)
                prak_set.add_entry('8.3.13', i, lupta, 'Lopa', l_exp)

                if l_exp[i - 1] in getPratyahara('?????????'):  # ????????????????????? ???????????????????????? ???????????????????????????
                    l_exp[i - 1] = getSvaraVariations(getBaseSvara(l_exp[i - 1]), 'Deergha')[0]
                    prak_set.add_entry('6.3.111', i - 1, l_exp[i - 1], 'Adesha', l_exp)

                return doSandhi(l_exp[:i], l_exp[i:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ?????? ??????
        if i == padanta and l_exp[i] == '??????' and l_exp[i + 1] == '??????' and (i, '8.3.14') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.14')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.14', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                lupta = l_exp.pop(i)
                prak_set.add_entry('8.3.14', i, lupta, 'Lopa', l_exp)

                if l_exp[i - 1] in getPratyahara('?????????'):  # ????????????????????? ???????????????????????? ???????????????????????????
                    l_exp[i - 1] = getSvaraVariations(getBaseSvara(l_exp[i - 1]), 'Deergha')[0]
                    prak_set.add_entry('6.3.111', i - 1, l_exp[i - 1], 'Adesha', l_exp)

                return doSandhi(l_exp[:i], l_exp[i:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ??????????????????????????? ??????????????????????????????
        if i == padanta and l_exp[i] == '??????' and l_exp[i + 1] in getPratyahara('?????????') and (i, '8.3.15') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.15')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.15', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = chr(2307)
                prak_set.add_entry('8.3.15', i, l_exp[i], 'Adesha', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ??????????????????????????????????????????????????? ???????????????
        if i + 1 == padanta and doVarnaMelana(l_exp[i: i + 2]) == '?????????' and l_exp[i - 1] in getSavarnas('???') and i != 0 and l_exp[i + 2] in getPratyahara('?????????') and (i, '8.3.17') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.17')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i + 1, '8.3.17', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = '??????'
                l_exp.pop(i + 1)
                prak_set.add_entry('8.3.17', i, l_exp[i], 'Adesha', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ???????????? ???????????????????????????
        if i == padanta and (l_exp[i] in ['??????', '??????'] and l_exp[i + 1] in getPratyahara('?????????')) and l_exp[i - 1] in getSavarnas('???') and i != 0 and not no_vikalpa and (i, '8.3.19') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.19')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.19', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                v_pset = prak_set.fork_new_with_entry('8.3.19', i, None, 'LopaVikalpa', list(l_exp))
                lupta = l_exp.pop(i)
                prak_set.add_entry('8.3.19', i, lupta, 'Lopa', l_exp)

                return doSandhi(l_exp[:i], l_exp[i:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ????????? ???????????????????????????
        if i == padanta and l_exp[i] == '??????' and l_exp[i + 1] in getPratyahara('?????????') and (i, '8.3.22') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.22')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.22', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                lupta = l_exp.pop(i)
                prak_set.add_entry('8.3.22', i, lupta, 'Lopa', l_exp)

                return doSandhi(l_exp[:i], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ?????????????????????????????????
        if i == padanta and l_exp[i] == '??????' and l_exp[i + 1] in getPratyahara('?????????') + ('??????',) and (i, '8.3.23') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.23')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.23', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = chr(2306)
                prak_set.add_entry('8.3.23', i, l_exp[i], 'Adesha', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ?????????????????????????????????????????? ?????????
        if i != padanta and l_exp[i] in ['??????', '??????'] and l_exp[i + 1] in getPratyahara('?????????') and (i, '8.3.24') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.24')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.24', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = chr(2306)
                prak_set.add_entry('8.3.24', i, l_exp[i], 'Adesha', l_exp)

                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ?????? ???????????? ??????
        if i == padanta and ord(l_exp[i][0]) == 2306 and l_exp[i + 1] == '??????' and l_exp[i + 2] in ['??????', '??????', '??????', '??????'] and not no_vikalpa and (i, '8.3.26') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.26')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.26', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                if l_exp[i + 2] == '??????':
                    l_exp[i] = '??????'
                else:
                    l_exp[i] = ['?????????', '?????????', '?????????'][['??????', '??????', '??????'].index(l_exp[i + 2])]
                prak_set.add_entry('8.3.26', i, l_exp[i], 'Adesha', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ???????????? ??????
        if i == padanta and ord(l_exp[i][0]) == 2306 and l_exp[i + 1] == '??????' and l_exp[i + 2] == '??????' and not no_vikalpa and (i, '8.3.27') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.27')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.27', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = '??????'
                prak_set.add_entry('8.3.27', i, l_exp[i], 'Adesha', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ??????????????? ???????????????????????? ?????????
        if i == padanta and l_exp[i] in ['??????', '??????'] and l_exp[i + 1] in getPratyahara('?????????') and not no_vikalpa and (i, '8.3.28') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.28')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.28', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                v_pset = prak_set.fork_new_with_entry('8.3.28', i, None, 'AgamaVikalpa', list(l_exp))
                l_exp.insert(i + 1, ['??????', '??????'][['??????', '??????'].index(l_exp[i])])
                prak_set.add_entry('8.3.28', i, doVarnaMelana([l_exp[i + 1]] + ['???', '??????']), 'Agama', l_exp)

                return doSandhi(l_exp[:i + 2], l_exp[i + 2:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ?????? ?????? ????????????, ????????????
        if i == padanta and l_exp[i] in ['??????', '??????'] and l_exp[i + 1] == '??????' and not no_vikalpa and ((l_exp[i] == '??????' and (i, '8.3.29') not in prak_set.l_lak_sutrams) or (l_exp[i] == '??????' and (i, '8.3.30') not in prak_set.l_lak_sutrams)):
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.29')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.29', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp.insert(i + 1, '??????')
                if l_exp[i] == '??????':
                    v_pset = prak_set.fork_new_with_entry('8.3.29', i + 1, None, 'AgamaVikalpa', list(l_exp))
                    prak_set.add_entry('8.3.29', i + 2, '????????????', 'Agama', l_exp)
                elif l_exp[i] == '??????':
                    v_pset = prak_set.fork_new_with_entry('8.3.30', i + 1, None, 'AgamaVikalpa', list(l_exp))
                    prak_set.add_entry('8.3.30', i + 2, '????????????', 'Agama', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ?????? ????????????
        if i == padanta and l_exp[i] == '??????' and l_exp[i + 1] == '??????' and not no_vikalpa and (i, '8.3.31') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.31')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.31', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                v_pset = prak_set.fork_new_with_entry('8.3.31', i, None, 'AgamaVikalpa', list(l_exp))
                l_exp.insert(i + 1, '??????')
                prak_set.add_entry('8.3.31', i, '????????????', 'Agama', l_exp)

                return doSandhi(l_exp[:i + 2], l_exp[i + 2:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ????????? ?????????????????????????????? ????????????????????????????????????
        if i == padanta and isHrsva(l_exp[i - 1]) and l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getPratyahara('?????????') and (i, '8.3.32') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.32')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.32', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp.insert(i, l_exp[i])
                prak_set.add_entry('8.3.32', i + 1, doVarnaMelana([l_exp[i]] + ['???', '??????']), 'Agama', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ???????????????????????????????????? ??????, ?????????????????? ??????????????????????????????, ?????? ?????????
        if i == padanta and l_exp[i] == chr(2307) and l_exp[i + 1] in getPratyahara('?????????') and (i, '8.3.34') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.3.34')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.3.34', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                if l_exp[i + 2] in getPratyahara('?????????') and (i, '8.3.35') not in prak_set.l_lak_sutrams:
                    prak_set.add_entry('8.3.35', i, l_exp[i], 'Adesha', l_exp)
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                if l_exp[i + 1] in getPratyahara('?????????') and (i, '8.3.36') not in prak_set.l_lak_sutrams:
                    v_pset = prak_set.fork_new_with_entry('8.3.36', i, None, 'AdeshaVikalpa', list(l_exp))
                    prak_set.add_entry('8.3.36', i, l_exp[i], 'Adesha', l_exp)
                    l_exp[i] = '??????'
                    v_pset.add_entry('8.3.34', i, l_exp[i], 'Adesha', l_exp)
                    return doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)
                if (i, '8.3.35') not in prak_set.l_lak_sutrams and (i, '8.3.36') not in prak_set.l_lak_sutrams:
                    l_exp[i] = '??????'
                    prak_set.add_entry('8.3.34', i, l_exp[i], 'Adesha', l_exp)
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ??????????????? ?????????????????? ???????????????
        if (l_exp[i] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????']) or (l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_exp[i] in ['??????', '??????', '??????', '??????', '??????', '??????']) and (i, '8.4.40') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.40')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.40', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                if not (l_exp[i] == '??????' and l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????']):
                    if l_exp[i] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????']:
                        l_exp[i] = ['??????', '??????', '??????', '??????', '??????', '??????'][['??????', '??????', '??????', '??????', '??????', '??????'].index(l_exp[i])]
                        prak_set.add_entry('8.4.40', i, l_exp[i], 'Adesha', l_exp)
                    elif l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_exp[i] in ['??????', '??????', '??????', '??????', '??????', '??????']:
                        l_exp[i + 1] = ['??????', '??????', '??????', '??????', '??????', '??????'][['??????', '??????', '??????', '??????', '??????', '??????'].index(l_exp[i + 1])]
                        prak_set.add_entry('8.4.40', i + 1, l_exp[i], 'Adesha', l_exp)
                else:
                    prak_set.add_entry('8.4.44', i + 1, None, 'Nishedha', l_exp)
                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ?????????????????? ???????????????
        if (l_exp[i] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????']) or (l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_exp[i] in ['??????', '??????', '??????', '??????', '??????', '??????']) and (i, '8.4.41') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.41')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.41', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                if l_exp[i] in getPratyahara('??????') and l_exp[i + 1] == '??????':
                    prak_set.add_entry('8.4.43', i, None, 'Nishedha', l_exp)
                elif i == padanta and l_exp[i] in getPratyahara('??????') and l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????']:
                    prak_set.add_entry('8.4.42', i + 1, None, 'Nishedha', l_exp)
                else:
                    if l_exp[i] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????']:
                        l_exp[i] = ['??????', '??????', '??????', '??????', '??????', '??????'][['??????', '??????', '??????', '??????', '??????', '??????'].index(l_exp[i])]
                        prak_set.add_entry('8.4.41', i, l_exp[i], 'Adesha', l_exp)
                    elif l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????', '??????'] and l_exp[i] in ['??????', '??????', '??????', '??????', '??????', '??????']:
                        l_exp[i + 1] = ['??????', '??????', '??????', '??????', '??????', '??????'][['??????', '??????', '??????', '??????', '??????', '??????'].index(l_exp[i + 1])]
                        prak_set.add_entry('8.4.41', i + 1, l_exp[i], 'Adesha', l_exp)

                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ???????????????????????????????????? ??????????????????????????? ??????
        if i == padanta and l_exp[i] in getPratyahara('?????????') and getSavarnas(l_exp[i]) and l_exp[i + 1] in ['??????', '??????', '??????', '??????', '??????', '?????????', '?????????', '?????????'] and (i, '8.4.45') not in prak_set.l_lak_sutrams and not no_vikalpa:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.45')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.45', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                v_pset = prak_set.fork_new_with_entry('8.4.45', i, None, 'AdeshaVikalpa', list(l_exp))
                l_exp[i] = getSavarnas(l_exp[i])[-1]
                prak_set.add_entry('8.4.45', i, l_exp[i], 'Adesha', l_exp)

                return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ????????? ???????????????????????? ????????????
        if i != padanta and l_exp[i - 2] in getPratyahara('?????????') + (chr(2306), ) and l_exp[i - 1] in ['??????', '??????'] and i >= 2 and l_exp[i] in getPratyahara('?????????') and not no_vikalpa and (i, '8.4.46') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.46')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.46', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                v_pset = prak_set.fork_new_with_entry('8.4.46', i, None, 'DvitvaVikalpa', list(l_exp))
                l_exp.insert(i + 1, l_exp[i])  # doing dvitva
                prak_set.add_entry('8.4.46', i, l_exp[i], 'Dvitva', l_exp)

                if padanta and i != padanta:
                    padanta = padanta + 1 if i < padanta else padanta
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)
                else:
                    return doSandhi(l_exp[:i + 2], l_exp[i + 2:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ???????????? ???
        if l_exp[i - 1] in getPratyahara('?????????') + (chr(2306), ) and i != 0 and l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] not in getPratyahara('?????????') and not no_vikalpa and (i, '8.4.47') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.47')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.47', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                v_pset = prak_set.fork_new_with_entry('8.4.47', i, None, 'DvitvaVikalpa', list(l_exp))
                l_exp.insert(i + 1, l_exp[i])  # doing dvitva
                prak_set.add_entry('8.4.47', i, l_exp[i], 'Dvitva', l_exp)

                if padanta and i != padanta:
                    padanta = padanta + 1 if i < padanta else padanta
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)
                else:
                    return doSandhi(l_exp[:i + 2], l_exp[i + 2:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ???????????? ????????? ?????????
        if l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getPratyahara('?????????') and (i, '8.4.53') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.53')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.53', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = getAdeshaBySthana([l_exp[i]], '?????????')
                prak_set.add_entry('8.4.53', i, l_exp[i], 'Adesha', l_exp)

                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ????????? ???
        if l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getPratyahara('?????????') and (i, '8.4.55') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.55')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.55', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = getAdeshaBySthana([l_exp[i]], '?????????')
                prak_set.add_entry('8.4.55', i, l_exp[i], 'Adesha', l_exp)

                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ????????????????????????????????? ????????? ????????????????????????,  ?????? ???????????????????????????
        if ord(l_exp[i][0]) == 2306 and l_exp[i + 1] in getPratyahara('?????????') and ((i != padanta and (i, '8.4.58') not in prak_set.l_lak_sutrams) or (i == padanta and (i, '8.4.59') not in prak_set.l_lak_sutrams and not no_vikalpa)):
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.58')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.58', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                adesha = getAdeshaBySthana([l_exp[i]], getSavarnas(l_exp[i + 1]))
                if adesha:
                    v_pset = prak_set.fork_new_with_entry('8.4.59', i, None, 'AdeshaVikalpa', list(l_exp))
                    l_exp[i] = adesha
                    if padanta and i != padanta:
                        prak_set.add_entry('8.4.58', i, l_exp[i], 'Adesha', l_exp)
                        return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                    else:
                        prak_set.add_entry('8.4.59', i, l_exp[i], 'Adesha', l_exp)
                        return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ??????????????????
        if l_exp[i] in getPratyahara('??????') and l_exp[i + 1] == '??????' and (i, '8.4.60') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.60')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.60', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                l_exp[i] = getAdeshaBySthana([l_exp[i]], ['??????', '?????????'])
                prak_set.add_entry('8.4.60', i, l_exp[i], 'Adesha', l_exp)

                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)

        # ????????? ??????????????????????????????????????????
        if l_exp[i - 1] in getPratyahara('?????????') and i != 0 and l_exp[i] == '??????' and (i, '8.4.62') not in prak_set.l_lak_sutrams and not no_vikalpa:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.62')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.62', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                v_pset = prak_set.fork_new_with_entry('8.4.62', i, None, 'AdeshaVikalpa', list(l_exp))
                l_exp[i] = getAdeshaBySthana(['??????'], getSavarnas(l_exp[i - 1]))
                prak_set.add_entry('8.4.62', i, l_exp[i], 'Adesha', l_exp)

                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ????????????????????????
        if l_exp[i - 1] in getPratyahara('?????????') and i != 0 and l_exp[i] == '??????' and l_exp[i + 1] in getPratyahara('?????????') and (i, '8.4.63') not in prak_set.l_lak_sutrams and not no_vikalpa:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.63')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.63', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                v_pset = prak_set.fork_new_with_entry('8.4.63', i, None, 'AdeshaVikalpa', list(l_exp))
                l_exp[i] = '??????'
                prak_set.add_entry('8.4.63', i, l_exp[i], 'Adesha', l_exp)

                if padanta and i != padanta:
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)
                else:
                    return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ????????? ???????????? ????????? ????????????
        if l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getPratyahara('?????????') and l_exp[i - 1] in getPratyahara('?????????') and i != 0 and not no_vikalpa and (i, '8.4.64') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.64')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.64', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                v_pset = prak_set.fork_new_with_entry('8.4.64', i, None, 'LopaVikalpa', list(l_exp))
                lupta = l_exp.pop(i)
                prak_set.add_entry('8.4.64', i, lupta, 'Lopa', l_exp)

                if padanta and i != padanta:
                    padanta = padanta - 1 if i < padanta else padanta
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)
                else:
                    return doSandhi(l_exp[:i], l_exp[i:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ????????? ????????? ??????????????????
        if l_exp[i] in getPratyahara('?????????') and l_exp[i + 1] in getPratyahara('?????????') and l_exp[i + 1] in getSavarnas(l_exp[i]) and l_exp[i - 1] in getPratyahara('?????????') and i != 0 and not no_vikalpa and (i, '8.4.65') not in prak_set.l_lak_sutrams:
            l_rightexp = getValidRoopa(prak_set.l_sutrams, prak_set.l_exps, '8.4.65')
            if l_rightexp == l_exp and not hasSiddhaAhead(l_exp1, l_exp2, i, '8.4.65', no_vikalpa, prak_set) and not (prak_set.l_prakriya and 'Prakrutibhava' in prak_set.l_prakriya[-1].Type and i == prak_set.l_prakriya[-1].Lakshyam):
                v_pset = prak_set.fork_new_with_entry('8.4.65', i, None, 'LopaVikalpa', list(l_exp))
                lupta = l_exp.pop(i)
                prak_set.add_entry('8.4.65', i, lupta, 'Lopa', l_exp)

                if padanta and i != padanta:
                    padanta = padanta - 1 if i < padanta else padanta
                    return doSandhi(l_exp[:padanta + 1], l_exp[padanta + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)
                else:
                    return doSandhi(l_exp[:i], l_exp[i:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set), doSandhi(l_exp1, l_exp2, at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=v_pset)

        # ?????????????????? ??????????????????????????? ?????????
        if i + 1 == padanta and doVarnaMelana(l_exp[i: i + 2]) == '?????????' and (i, '?????????', 'Adesha') in prak_set.l_lak_vis_types:
            lupta = l_exp.pop(i + 1)
            prak_set.add_entry('1.3.09', i + 1, lupta, 'Lopa', l_exp)  # ???????????? ????????????
            return doSandhi(l_exp[:i + 1], l_exp[i + 1:], at_padanta=at_padanta, no_vikalpa=no_vikalpa, prakriya=prak_set)
    else:
        # ????????? ?????????
        if l_exp[i + 1] in getPratyahara('??????') and (i + 1, '8.2.30') not in prak_set.l_lak_sutrams:
            l_exp[i + 1] = getPratyahara('??????')[getPratyahara('??????').index(l_exp[i])]
            prak_set.add_entry('8.2.30', i + 1, l_exp[i + 1], 'Adesha', l_exp)

        # ???????????? ????????????????????????
        if l_exp[i + 1] in getPratyahara('?????????') and l_exp[i + 1] not in ['??????', '??????', '??????'] and (i + 1, '8.2.39') not in prak_set.l_lak_sutrams:
            l_exp[i + 1] = getAdeshaBySthana([l_exp[i + 1]], '?????????')
            prak_set.add_entry('8.2.39', i + 1, l_exp[i + 1], 'Adesha', l_exp)

        # ?????????????????? ?????????
        if l_exp[i + 1] == '??????' and (i + 1, '8.2.66') not in prak_set.l_lak_sutrams:
            l_exp[i + 1] = '??????'
            prak_set.add_entry('8.2.66', i + 1, '?????????', 'Adesha', l_exp)
            prak_set.add_entry('1.3.09', i + 2, '??????', 'Lopa', l_exp)

        # ??????????????????????????? ??????????????????????????????
        if l_exp[i + 1] == '??????' and (i + 1, '8.3.15') not in prak_set.l_lak_sutrams:
            l_exp[i + 1] = chr(2307)
            prak_set.add_entry('8.3.15', i + 1, l_exp[i + 1], 'Adesha', l_exp)

        return doVarnaMelana(l_exp)

if __name__ == '__main__':
    res = doSandhi('???????????????', '????????????', no_vikalpa=False)
    if isinstance(res, tuple):
        print(flatten_and_set(res))
    else:
        print(res)
