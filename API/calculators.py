from typing import Dict, Union


class Calculators:

    @staticmethod
    def calculate_1rm_logic(lifted_weight: float, reps: int) -> float:
        """
            Calculate one rep max weight for the given data.
        :param lifted_weight: lifted weight
        :param reps: reps amount
        :return: one rep max weight for the data provided
        """

        if reps == 1:
            result = lifted_weight
        else:
            result = lifted_weight * (1 + 0.03 * reps)

        result = round(result, 2)
        return result

    @staticmethod
    def calculate_wilks_logic(is_female: bool, body_weight: float, lifted_weight: float) -> float:
        """
            Calculate Wilks points for the given data.
        :param is_female: if female type True else type False
        :param body_weight: body weight
        :param lifted_weight: lifted weight
        :return: wilks points for the provided data
        """

        a0, a1, a2, a3, a4, a5 = -125.4255398, 13.71219419, -0.03307250631, -0.1050400051E-2, \
            0.938773881462799E-5, -0.23334613884954E-7  # women
        b0, b1, b2, b3, b4, b5 = 47.46178854, 8.472061379, 0.07369410346, -0.001395833811, \
            0.707665973070743E-5, -0.120804336482315E-7  # men

        if is_female:
            coefficients = [a0, a1, a2, a3, a4, a5]
        else:
            coefficients = [b0, b1, b2, b3, b4, b5]

        coefficients_sum = sum(c * body_weight ** i for i, c in enumerate(coefficients))
        result = lifted_weight * (600 / coefficients_sum)
        result = round(result, 2)

        return result

    @staticmethod
    def calculate_dots_logic(is_female: bool, body_weight: float, lifted_weight: float) -> float:
        """
            Calculate DOTS points for the given data.
        :param is_female: if female type True else type False
        :param body_weight: body weight
        :param lifted_weight: lifted weight
        :return: DOTS points for the data provided
        """

        a0, a1, a2, a3, a4 = -57.96288, 13.6175032, -0.1126655495, 0.0005158568, -0.0000010706  # women
        b0, b1, b2, b3, b4 = -307.75076, 24.0900756, -0.1918759221, 0.0007391293, -0.000001093  # men

        if is_female:
            coefficients = [a0, a1, a2, a3, a4]
        else:
            coefficients = [b0, b1, b2, b3, b4]

        coefficients_sum = sum(c * body_weight ** i for i, c in enumerate(coefficients))
        result = lifted_weight * (500 / coefficients_sum)
        result = round(result, 2)

        return result

    @staticmethod
    def calculate_ipf_gl_logic(is_female: bool, body_weight: float, lifted_weight: float) -> float:
        """
            Calculate IPF GL points for the given data.
        :param is_female: if female type True else type False
        :param body_weight: body weight
        :param lifted_weight: lifted weight
        :return: IPF GL points for the data provided
        """

        a0, a1, a2 = 610.32796, 1045.59282, 0.03048  # women
        b0, b1, b2 = 1199.72839, 1025.18162, 0.00921  # men

        if is_female:
            coefficients = [a0, a1, a2]
        else:
            coefficients = [b0, b1, b2]

        coefficients_sum = coefficients[0] - coefficients[1] * 2.71828 ** ((-coefficients[2]) * body_weight)
        result = lifted_weight * (100 / coefficients_sum)
        result = round(result, 2)

        return result

    @staticmethod
    def total_logic(is_female: bool, body_weight: float, squat_weight: float, squat_reps: int, bench_weight: float,
                    bench_reps: int, deadlift_weight: float, deadlift_reps: int) -> Dict[str, Union[str, int, float]]:
        """
        Calculate one rep maxes, total and points(WILKS, DOTS, IPF GL) for the given data.
        """

        squat_max = Calculators.calculate_1rm_logic(lifted_weight=squat_weight, reps=squat_reps)
        squat_wilks = Calculators.calculate_wilks_logic(is_female=is_female, body_weight=body_weight,
                                                        lifted_weight=squat_max)
        squat_dots = Calculators.calculate_dots_logic(is_female=is_female, body_weight=body_weight,
                                                      lifted_weight=squat_max)
        squat_ipf_gl = Calculators.calculate_ipf_gl_logic(is_female=is_female, body_weight=body_weight,
                                                          lifted_weight=squat_max)

        bench_max = Calculators.calculate_1rm_logic(lifted_weight=bench_weight, reps=bench_reps)
        bench_wilks = Calculators.calculate_wilks_logic(is_female=is_female, body_weight=body_weight,
                                                        lifted_weight=bench_max)
        bench_dots = Calculators.calculate_dots_logic(is_female=is_female, body_weight=body_weight,
                                                      lifted_weight=bench_max)
        bench_ipf_gl = Calculators.calculate_ipf_gl_logic(is_female=is_female, body_weight=body_weight,
                                                          lifted_weight=bench_max)

        deadlift_max = Calculators.calculate_1rm_logic(lifted_weight=deadlift_weight, reps=deadlift_reps)
        deadlift_wilks = Calculators.calculate_wilks_logic(is_female=is_female, body_weight=body_weight,
                                                           lifted_weight=deadlift_max)
        deadlift_dots = Calculators.calculate_dots_logic(is_female=is_female, body_weight=body_weight,
                                                         lifted_weight=deadlift_max)
        deadlift_ipf_gl = Calculators.calculate_ipf_gl_logic(is_female=is_female, body_weight=body_weight,
                                                             lifted_weight=deadlift_max)

        total = sum([squat_max, bench_max, deadlift_max])
        total_wilks = Calculators.calculate_wilks_logic(is_female=is_female, body_weight=body_weight,
                                                        lifted_weight=total)
        total_dots = Calculators.calculate_dots_logic(is_female=is_female, body_weight=body_weight, lifted_weight=total)
        total_ipf_gl = Calculators.calculate_ipf_gl_logic(is_female=is_female, body_weight=body_weight,
                                                          lifted_weight=total)

        return {
            'gender': 'female' if is_female else 'male',
            'weight': body_weight,
            'squat': squat_max,
            'squat_wilks': squat_wilks,
            'squat_dots': squat_dots,
            'squat_ipf_gl': squat_ipf_gl,
            'bench': bench_max,
            'bench_wilks': bench_wilks,
            'bench_dots': bench_dots,
            'bench_ipf_gl': bench_ipf_gl,
            'deadlift': deadlift_max,
            'deadlift_wilks': deadlift_wilks,
            'deadlift_dots': deadlift_dots,
            'deadlift_ipf_gl': deadlift_ipf_gl,
            'total': total,
            'total_wilks': total_wilks,
            'total_dots': total_dots,
            'total_ipf_gl': total_ipf_gl,
        }
