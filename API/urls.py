from django.urls import path
from .views import GetAllBodyParts, Calculate1RM, CalculateWilks, CalculateDots, CalculateIpfGl, CalculateTotal,\
     ReadPrivateExercises, ReadPublicExercises, CreatePrivateExercise, DeletePrivateExercise, UpdatePrivateExercise,\
     ReadUserTrainingPlans, CreateUserTrainingPlan, UpdateUserTrainingPlan, DeleteUserTrainingPlan, CreateTraining,\
     ReadTrainings, UpdateTraining, DestroyTraining, CreateTrainingRecord, ReadTrainingRecord, UpdateTrainingRecord,\
     DestroyTrainingRecord, CreateTrainingExercise, ReadTrainingExercise, UpdateTrainingExercise,\
     DestroyTrainingExercise, CreateTrainingPlanExerciseInfo, ReadTrainingPlanExerciseInfo,\
    UpdateTrainingPlanExerciseInfo, DestroyTrainingPlanExerciseInfo, UserRegister
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', UserRegister.as_view(), name='user-register'),

    #Calculators
    path('1rm/', Calculate1RM.as_view(), name='calculate-1rm'),
    path('wilks/', CalculateWilks.as_view(), name='calculate-wilks'),
    path('dots/', CalculateDots.as_view(), name='calculate-dots'),
    path('ipfgl/', CalculateIpfGl.as_view(), name='calculate-ipf-gl'),
    path('total/', CalculateTotal.as_view(), name='calculate-total'),

    #CRUD for exercises
    path('bodyparts/', GetAllBodyParts.as_view(), name='read-all-body-parts'),
    path('createexercises/', CreatePrivateExercise.as_view(), name='create-exercise'), # exercises -> POST
    path('exercises/public/', ReadPublicExercises.as_view(), name='read-public-exercises'), # exercises/public - GET
    path('exercises/private/', ReadPrivateExercises.as_view(), name='read-private-exercises'), # exercises/<int:user>/private/ - GET DEATIL
    path('updateexercises/<int:pk>', UpdatePrivateExercise.as_view(), name='update-private-exercise'), # exercises/<int:pk>  -> PUT / PATCH
    path('deleteexercises/<int:pk>', DeletePrivateExercise.as_view(), name='delete-exercise'),  # exercises/<int:pk> -> DELETE

    #CRUD for usertrainingplans
    path('createusertrainingplan/', CreateUserTrainingPlan.as_view(), name='create-user-training-plan'), #  training-plans -> POST
    path('readusertrainingplans/', ReadUserTrainingPlans.as_view(), name='read-user-training-plans'),
    path('updateusertrainingplan/<int:pk>', UpdateUserTrainingPlan.as_view(), name='update-user-training-plan'),
    path('deleteusertrainingplan/<int:pk>', DeleteUserTrainingPlan.as_view(), name='delete-user-training-plan'),

    #CRUD for trainings
    path('createtraining/', CreateTraining.as_view(), name='create-training'),
    path('readtrainings/', ReadTrainings.as_view(), name='read-trainings'),
    path('updatetraining/<int:pk>', UpdateTraining.as_view(), name='update-training'),
    path('deletetraining/<int:pk>', DestroyTraining.as_view(), name='delete-training'),

    #CRUD for trainingrecord
    path('createtrainingrecord/', CreateTrainingRecord.as_view(), name='create-training-record'),
    path('readtrainingrecord/', ReadTrainingRecord.as_view(), name='read-training-record'),
    path('updatetrainingrecord/<int:pk>', UpdateTrainingRecord.as_view(), name='update-training-record'),
    path('deletetrainingrecord/<int:pk>', DestroyTrainingRecord.as_view(), name='delete-training-record'),

    #CRUD for trainingexercise
    path('createtrainingexercise/', CreateTrainingExercise.as_view(), name='create-training-exercise'),
    path('readtrainingexercise/', ReadTrainingExercise.as_view(), name='read-training-exercise'),
    path('updatetrainingexercise/<int:pk>', UpdateTrainingExercise.as_view(), name='update-training-exercise'),
    path('deletetrainingexercise/<int:pk>', DestroyTrainingExercise.as_view(), name='delete-training-exercise'),

    #CRUD for trainingplanexerciseinfo
    path('createtrainingplanexerciseinfo/', CreateTrainingPlanExerciseInfo.as_view(),
         name='create-training-plan-exercise-info'),
    path('readtrainingplanexerciseinfo/', ReadTrainingPlanExerciseInfo.as_view(),
         name='read-training-plan-exercise-info'),
    path('updatetrainingplanexerciseinfo/<int:pk>', UpdateTrainingPlanExerciseInfo.as_view(),
         name='update-training-plan-exercise-info'),
    path('deletetrainingplanexerciseinfo/<int:pk>', DestroyTrainingPlanExerciseInfo.as_view(),
         name='destroy-training-plan-exercise-info'),


]
