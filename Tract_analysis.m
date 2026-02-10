% Automated script that matches the EDTI GUI functionality
% Load .mat DTI file
% Load tractography
% Load ROIs
% Analyze tracs
% Save tracs
% Same input/output directory
% Save analysed tracts in two different directories
% 1) The same directory as whole brain tract files for
% optimization/visualization/validation
% 2) The directory for further segmentation


%input_path = 'H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Tract_analysis\Left\continue';
input_path = 'H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Tract_analysis\Right';
subfolders = dir(fullfile(input_path, '*'));
%input_path_segm = 'H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Segmentation\Left\continue';
input_path_segm = 'H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Segmentation\Right';

for i= 1:length(subfolders)
   if subfolders(i).isdir && ~strcmp(subfolders(i).name, '.') && ~strcmp(subfolders(i).name, '..') 
        subject_name = subfolders(i).name; %extract subject name
        dti_filename = [subject_name, '_MD_C_native.mat'];
        tract_filename = [subject_name, '_MD_C_native_Tracts_DTI.mat'];
        save_tract_filename = [subject_name, '_MD_C_native_Tracts_DTI_Save.mat'];   
        
        % Call EDTI functions
        E_DTI_Load_DTI_data_from_mat_file(fullfile(input_path, subject_name), dti_filename);
        E_DTI_Load_Multiple_ROI(fullfile(input_path, subject_name));
        E_DTI_Load_Tracts(fullfile(input_path, subject_name), tract_filename);

        E_DTI_Analyse_tracts_new; %for splitting tracts
        % include draw trac (for optimization and validation)    
        E_DTI_Draw_Tracts;
        E_DTI_Save_Tracts(fullfile(input_path, subject_name), save_tract_filename);
        E_DTI_Save_Tracts(fullfile(input_path_segm, subject_name), save_tract_filename);        
        % Delete_ROIs to delete previous ROIs and load the next ones. 
        % DONT FORGET TO select the ALL square at EDTI
        
        E_DTI_Delete_ROI('SEED')
        E_DTI_Delete_ROI('AND')
        E_DTI_Delete_Tracts % Delete tracs in order to load the tracs of the next subject
        
        % Will add if Tracts exists then print succesfull
        fprintf('Tract analysis for subject %s is successful.\n', subject_name);
   end   
end






