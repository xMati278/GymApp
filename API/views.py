from rest_framework.decorators import api_view
from rest_framework.response import Response
from http import HTTPStatus
from .calculators import Calculators
# Create your views here.


@api_view(['GET'])
def calculate_1rm(request) -> Response:
    """
        Validate, calculates and returns one rep max weight for the given data.
    :return: Response with one rep max weight with key '1rm'
    """

    reps = request.GET.get('reps')
    lifted_weight = request.GET.get('weight')

    data_dict = Calculators.validate_calculator_data(reps=reps, lifted_weight=lifted_weight, one_rm_calc=True)
    if 'error' in data_dict:
        return Response({'error': data_dict['error']}, status=HTTPStatus.BAD_REQUEST)

    reps, lifted_weight = data_dict['reps'], data_dict['lifted_weight']

    result = Calculators.calculate_1rm_logic(lifted_weight, reps)
    return Response({'1rm': result}, status=HTTPStatus.OK)


@api_view(['GET'])
def calculate_wilks(request) -> Response:
    """
        Validate, calculates and returns wilks points for the given data.
    :return: Response with wilks points with key 'wilks'
    """

    is_female = request.GET.get('female')
    body_weight = request.GET.get('body')
    lifted_weight = request.GET.get('lift')

    data_dict = Calculators.validate_calculator_data(is_female=is_female, body_weight=body_weight,
                                         lifted_weight=lifted_weight)
    if 'error' in data_dict:
        return Response({'error': data_dict['error']}, status=HTTPStatus.BAD_REQUEST)

    is_female, body_weight, lifted_weight = data_dict['is_female'], data_dict['body_weight'],\
        data_dict['lifted_weight']

    wilks = Calculators.calculate_wilks_logic(is_female=is_female, body_weight=body_weight, lifted_weight=lifted_weight)

    return Response({'wilks': wilks}, status=HTTPStatus.OK)


@api_view(['GET'])
def calculate_dots(request) -> Response:
    """
        Validate, calculates and returns dots points for the given data.
    :return: Response with DOTS points with key 'dots'
    """

    is_female = request.GET.get('female')
    body_weight = request.GET.get('body')
    lifted_weight = request.GET.get('lift')

    data_dict = Calculators.validate_calculator_data(is_female=is_female, body_weight=body_weight,
                                         lifted_weight=lifted_weight)
    if 'error' in data_dict:
        return Response({'error': data_dict['error']}, status=HTTPStatus.BAD_REQUEST)

    is_female, body_weight, lifted_weight = data_dict['is_female'], data_dict['body_weight'],\
        data_dict['lifted_weight']

    dots = Calculators.calculate_dots_logic(is_female=is_female, body_weight=body_weight, lifted_weight=lifted_weight)

    return Response({'dots': dots}, status=HTTPStatus.OK)


@api_view(['GET'])
def calculate_ipf_gl(request) -> Response:
    """
        Validate, calculates and returns IPF GL for the given data.
    :return: Response with DOTS points with key 'ipf_gl'
    """

    is_female = request.GET.get('female')
    body_weight = request.GET.get('body')
    lifted_weight = request.GET.get('lift')

    data_dict = Calculators.validate_calculator_data(is_female=is_female, body_weight=body_weight,
                                         lifted_weight=lifted_weight)
    if 'error' in data_dict:
        return Response({'error': data_dict['error']}, status=HTTPStatus.BAD_REQUEST)

    is_female, body_weight, lifted_weight = data_dict['is_female'], data_dict['body_weight'],\
        data_dict['lifted_weight']

    ipfgl = Calculators.calculate_ipf_gl_logic(is_female=is_female, body_weight=body_weight, lifted_weight=lifted_weight)

    return Response({'ipf_gl': ipfgl}, status=HTTPStatus.OK)


@api_view(['GET'])
def calculate_total(request) -> Response:
    """
        Validate, calculates and returns one rep maxes, total and points(WILKS, DOTS, IPF GL) for the given data.
    :return: Response with one rep maxes, total and points(WILKS, DOTS, IPF GL)
    """

    is_female = request.GET.get('female')
    body_weight = request.GET.get('body')
    squat_weight = request.GET.get('sq')
    squat_reps = request.GET.get('sq-reps')
    bench_weight = request.GET.get('bp')
    bench_reps = request.GET.get('bp-reps')
    deadlift_weight = request.GET.get('dl')
    deadlift_reps = request.GET.get('dl-reps')

    data_dict = Calculators.validate_total_data(is_female=is_female, body_weight=body_weight, squat_weight=squat_weight,
                                    squat_reps=squat_reps, bench_weight=bench_weight, bench_reps=bench_reps,
                                    deadlift_weight=deadlift_weight, deadlift_reps=deadlift_reps)
    if 'error' in data_dict:
        return Response({'error': data_dict['error']}, status=HTTPStatus.BAD_REQUEST)

    is_female, body_weight, squat_weight, squat_reps, bench_weight, bench_reps, deadlift_weight, deadlift_reps = \
        data_dict['is_female'], data_dict['body_weight'], data_dict['squat_weight'], data_dict['squat_reps'],\
        data_dict['bench_weight'], data_dict['bench_reps'], data_dict['deadlift_weight'], data_dict['deadlift_reps']

    total = Calculators.total_logic(is_female=is_female, body_weight=body_weight, squat_weight=squat_weight, squat_reps=squat_reps,
                        bench_weight=bench_weight, bench_reps=bench_reps, deadlift_weight=deadlift_weight,
                        deadlift_reps=deadlift_reps)

    return Response(total, status=HTTPStatus.OK)
