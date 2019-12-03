def ImportAllAssets():
#This script was generated with the addons Blender for UnrealEngine : https://github.com/xavier150/Blender-For-UnrealEngine-Addons
#This script will import in unreal all camera in target sequencer
#The script must be used in Unreal Engine Editor with UnrealEnginePython : https://github.com/20tab/UnrealEnginePython
#Use this command : unreal_engine.py_exec(r"D:\2019au\etgg3801\assets\ExportedFbx\ImportAssetScript.py")


	import os.path
	import configparser
	import ast
	import unreal_engine as ue
	from unreal_engine.classes import PyFbxFactory, AlembicImportFactory, StaticMesh, Skeleton, SkeletalMeshSocket
	from unreal_engine.enums import EFBXImportType, EMaterialSearchLocation, ECollisionTraceFlag
	from unreal_engine.structs import StaticMeshSourceModel, MeshBuildSettings
	from unreal_engine import FVector, FRotator
	
	
	#Prepare var and def
	unrealImportLocation = r'/Game/ImportedFbx'
	ImportedList = []
	ImportFailList = []
	
	def GetOptionByIniFile(FileLoc, OptionName, literal = False):
		Config = configparser.ConfigParser()
		Config.read(FileLoc)
		Options = []
		if Config.has_section(OptionName):
			for option in Config.options(OptionName):
				if (literal == True):
					Options.append(ast.literal_eval(Config.get(OptionName, option)))
				else:
					Options.append(Config.get(OptionName, option))
		else:
			print("/!\ Option: "+OptionName+" not found in file: "+FileLoc)
		return Options
	
	
	#Process import
	print('========================= Import started ! =========================')
	
	
	
	
	'''
	<################################################################################>
	<#############################	             		#############################>
	<############################	             		 ############################>
	<############################	 SkeletalMesh tasks	 ############################>
	<############################	             		 ############################>
	<#############################	             		#############################>
	<################################################################################>
	'''
	
	SkeletalMesh_TasksList = []
	SkeletalMesh_PreImportPath = []
	print('========================= Creating SkeletalMesh tasks... =========================')
	
	def CreateTask_SK_Armature():
		################[ Import Armature as SkeletalMesh type ]################
		print('================[ New import task : Armature as SkeletalMesh type ]================')
		FilePath = os.path.join(r'D:\2019au\etgg3801\assets\ExportedFbx\SkeletalMesh\Armature\SK_Armature.fbx')
		AdditionalParameterLoc = os.path.join(r'D:\2019au\etgg3801\assets\ExportedFbx\SkeletalMesh\Armature\SK_Armature_AdditionalParameter.ini')
		AssetImportPath = (os.path.join(unrealImportLocation, r'').replace('\\','/')).rstrip('/')
		task = PyFbxFactory()
		task.ImportUI.MeshTypeToImport = EFBXImportType.FBXIT_SkeletalMesh
		task.ImportUI.bImportMaterials = True
		task.ImportUI.bImportTextures = False
		task.ImportUI.bImportAnimations = False
		task.ImportUI.bCreatePhysicsAsset = True
		task.ImportUI.bImportAnimations = False
		task.ImportUI.bImportMesh = True
		task.ImportUI.bCreatePhysicsAsset = True
		task.ImportUI.TextureImportData.MaterialSearchLocation = EMaterialSearchLocation.Local
		task.ImportUI.SkeletalMeshImportData.bImportMorphTargets = True
		print('================[ import asset : Armature ]================')
		try:
			asset = task.factory_import_object(FilePath, AssetImportPath)
		except:
			asset = None
		if asset == None:
			ImportFailList.append('Asset "Armature" not found for after inport')
			return
		print('========================= Imports of Armature completed ! Post treatment started...	=========================')
		skeleton = asset.skeleton
		current_sockets = skeleton.Sockets
		new_sockets = []
		sockets_to_add = GetOptionByIniFile(AdditionalParameterLoc, 'Sockets', True)
		for socket in sockets_to_add :
			#Create socket
			new_socket = SkeletalMeshSocket('', skeleton)
			new_socket.SocketName = socket[0]
			print(socket[0])
			new_socket.BoneName = socket[1]
			l = socket[2]
			r = socket[3]
			s = socket[4]
			new_socket.RelativeLocation = FVector(l[0], l[1], l[2])
			new_socket.RelativeRotation = FRotator(r[0], r[1], r[2])
			new_socket.RelativeScale = FVector(s[0], s[1], s[2])
			new_sockets.append(new_socket)
		skeleton.Sockets = new_sockets
		
		lods_to_add = GetOptionByIniFile(AdditionalParameterLoc, 'LevelOfDetail')
		for x, lod in enumerate(lods_to_add):
			pass
		print('========================= Post treatment of Armature completed !	 =========================')
		asset.save_package()
		asset.post_edit_change()
		ImportedList.append([asset, 'SkeletalMesh'])
	CreateTask_SK_Armature()
	
	
	
	
	
	'''
	<#############################################################################>
	<#############################	          		#############################>
	<############################	          		 ############################>
	<############################	 Animation tasks	 ############################>
	<############################	          		 ############################>
	<#############################	          		#############################>
	<#############################################################################>
	'''
	
	Animation_TasksList = []
	Animation_PreImportPath = []
	print('========================= Creating Animation tasks... =========================')
	
	def CreateTask_Anim_Armature_Idle():
		################[ Import Armature as Action type ]################
		print('================[ New import task : Armature as Action type ]================')
		FilePath = os.path.join(r'D:\2019au\etgg3801\assets\ExportedFbx\SkeletalMesh\Armature\Anim\Anim_Armature_Idle.fbx')
		AdditionalParameterLoc = os.path.join(r'D:\2019au\etgg3801\assets\ExportedFbx\SkeletalMesh\Armature\Anim\SK_Armature_AdditionalParameter.ini')
		AssetImportPath = (os.path.join(unrealImportLocation, r'Anim').replace('\\','/')).rstrip('/')
		SkeletonLocation = os.path.join(unrealImportLocation, r'SK_Armature_Skeleton.SK_Armature_Skeleton').replace('\\','/')
		OriginSkeleton = ue.find_asset(SkeletonLocation)
		task = PyFbxFactory()
		if OriginSkeleton:
			task.ImportUI.Skeleton = OriginSkeleton
		else:
			ImportFailList.append('Skeleton "'+SkeletonLocation+'" Not found for "Armature" asset ')
			return
		task.ImportUI.MeshTypeToImport = EFBXImportType.FBXIT_Animation
		task.ImportUI.bImportMaterials = False
		task.ImportUI.bImportTextures = False
		task.ImportUI.bImportAnimations = True
		task.ImportUI.bImportMesh = False
		task.ImportUI.bCreatePhysicsAsset = False
		task.ImportUI.SkeletalMeshImportData.bImportMorphTargets = True
		print('================[ import asset : Armature ]================')
		try:
			asset = task.factory_import_object(FilePath, AssetImportPath)
		except:
			asset = None
		if asset == None:
			ImportFailList.append('Asset "Armature" not found for after inport')
			return
		print('========================= Imports of Armature completed ! Post treatment started...	=========================')
		print('========================= Post treatment of Armature completed !	 =========================')
		asset.save_package()
		asset.post_edit_change()
		ImportedList.append([asset, 'Action'])
	CreateTask_Anim_Armature_Idle()
	
	
	
	
	def CreateTask_Anim_Armature_Walk():
		################[ Import Armature as Action type ]################
		print('================[ New import task : Armature as Action type ]================')
		FilePath = os.path.join(r'D:\2019au\etgg3801\assets\ExportedFbx\SkeletalMesh\Armature\Anim\Anim_Armature_Walk.fbx')
		AdditionalParameterLoc = os.path.join(r'D:\2019au\etgg3801\assets\ExportedFbx\SkeletalMesh\Armature\Anim\SK_Armature_AdditionalParameter.ini')
		AssetImportPath = (os.path.join(unrealImportLocation, r'Anim').replace('\\','/')).rstrip('/')
		SkeletonLocation = os.path.join(unrealImportLocation, r'SK_Armature_Skeleton.SK_Armature_Skeleton').replace('\\','/')
		OriginSkeleton = ue.find_asset(SkeletonLocation)
		task = PyFbxFactory()
		if OriginSkeleton:
			task.ImportUI.Skeleton = OriginSkeleton
		else:
			ImportFailList.append('Skeleton "'+SkeletonLocation+'" Not found for "Armature" asset ')
			return
		task.ImportUI.MeshTypeToImport = EFBXImportType.FBXIT_Animation
		task.ImportUI.bImportMaterials = False
		task.ImportUI.bImportTextures = False
		task.ImportUI.bImportAnimations = True
		task.ImportUI.bImportMesh = False
		task.ImportUI.bCreatePhysicsAsset = False
		task.ImportUI.SkeletalMeshImportData.bImportMorphTargets = True
		print('================[ import asset : Armature ]================')
		try:
			asset = task.factory_import_object(FilePath, AssetImportPath)
		except:
			asset = None
		if asset == None:
			ImportFailList.append('Asset "Armature" not found for after inport')
			return
		print('========================= Imports of Armature completed ! Post treatment started...	=========================')
		print('========================= Post treatment of Armature completed !	 =========================')
		asset.save_package()
		asset.post_edit_change()
		ImportedList.append([asset, 'Action'])
	CreateTask_Anim_Armature_Walk()
	
	
	
	
	print('========================= Full import completed !  =========================')
	
	StaticMesh_ImportedList = []
	SkeletalMesh_ImportedList = []
	Alembic_ImportedList = []
	Animation_ImportedList = []
	for asset in ImportedList:
		if asset[1] == 'StaticMesh':
			StaticMesh_ImportedList.append(asset[0])
		elif asset[1] == 'SkeletalMesh':
			SkeletalMesh_ImportedList.append(asset[0])
		elif asset[1] == 'Alembic':
			Alembic_ImportedList.append(asset[0])
		else:
			Animation_ImportedList.append(asset[0])
	
	print('Imported StaticMesh: '+str(len(StaticMesh_ImportedList)))
	print('Imported SkeletalMesh: '+str(len(SkeletalMesh_ImportedList)))
	print('Imported Alembic: '+str(len(Alembic_ImportedList)))
	print('Imported Animation: '+str(len(Animation_ImportedList)))
	print('Import failled: '+str(len(ImportFailList)))
	for error in ImportFailList:
		print(error)
	
	#Select asset(s) in content browser
	PathList = []
	for asset in (StaticMesh_ImportedList + SkeletalMesh_ImportedList + Alembic_ImportedList + Animation_ImportedList):
		PathList.append(asset.get_path_name())
	
	print('=========================')
	if len(ImportFailList) == 0:
		return 'Assets imported with success !' 
	else:
		return 'Some asset(s) could not be imported.' 
	
print(ImportAllAssets())
