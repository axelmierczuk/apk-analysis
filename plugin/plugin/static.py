from typing import List

from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat, EncodedMethod, DalvikCode, ClassDefItem, ClassDataItem, \
    EncodedField
from androguard.core.analysis.analysis import Analysis, MethodClassAnalysis, ClassAnalysis
from androguard.decompiler.decompiler import DecompilerJADX
from androguard.core.androconf import show_logging
import logging

show_logging(level=logging.ERROR)


class StaticAnalysis:
    def analyze(self, file: str):
        a = APK(file)
        d = DalvikVMFormat(a)

        res = {}

        permissions = a.get_permissions()
        activities = a.get_activities()
        methods = d.get_methods()
        classes = d.get_classes()
        # methods = dx.get_methods()
        class_feats = self.analyze_classes(classes=classes)
        method_feats = self.analyze_methods(methods=methods)
        for permission in permissions:
            res[f'permission_{permission}'] = int(True)
        res['num_activities'] = len(activities)
        res['total_classes'] = len(classes)

        return res, class_feats, method_feats

    @staticmethod
    def analyze_classes(classes: List[ClassDefItem]):
        class_feats = []
        for c in classes:
            tmp_res_class = dict()
            tmp_res_class['name'] = c.name
            tmp_res_class['num_methods'] = len(c.get_methods())
            tmp_res_class['num_fields'] = len(c.get_fields())
            tmp_res_class['access_flags'] = c.get_access_flags()
            class_data: ClassDataItem = c.get_class_data()
            if class_data:
                tmp_res_class['num_direct_methods'] = len(class_data.get_direct_methods())
                tmp_res_class['num_static_fields'] = len(class_data.get_static_fields())
                tmp_res_class['num_virtual_methods'] = len(class_data.get_virtual_methods())
            tmp_res_class['num_fields'] = len(c.get_fields())

            class_feats.append(tmp_res_class)

        return class_feats

    @staticmethod
    def analyze_methods(methods: List[EncodedMethod]):
        method_feats = []

        for method in methods:
            tmp_res = dict()
            tmp_res['name'] = method.name
            tmp_res['access_flags'] = method.access_flags
            code: DalvikCode = method.get_code()
            if code:
                tmp_res['size'] = code.get_size()
                tmp_res['registers_size'] = code.get_registers_size()
                tmp_res['ins_size'] = code.get_ins_size()
                tmp_res['outs_size'] = code.get_outs_size()
                tmp_res['tries_size'] = code.get_tries_size()
            else:
                tmp_res['size'] = 0
                tmp_res['registers_size'] = 0
                tmp_res['ins_size'] = 0
                tmp_res['outs_size'] = 0
                tmp_res['tries_size'] = 0
            method_feats.append(tmp_res)

        return method_feats



