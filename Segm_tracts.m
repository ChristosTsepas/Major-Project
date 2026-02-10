% MATLAB script to segment tracts based on the ExploreDTI functionality and GUI

%input_path = 'H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Segmentation\Left';
input_path = 'H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Segmentation\Right';
subfolders = dir(fullfile(input_path, '*'));


%input_path_segm = 'H:\Marc_Pastur_pipeline\DTI_MODEL\Segmentation\Left';
input_path_segm = 'H:\Marc_Pastur_pipeline\DTI_MODEL\Segmentation\Right';


% Initialize an empty cell array to store subject names without tracts
no_tract_subjects = {};

% DON'T FORGET TO CHECK THE SEGMENT ONLY BUTTON

for i = 1:length(subfolders)
    if subfolders(i).isdir && ~strcmp(subfolders(i).name, '.') && ~strcmp(subfolders(i).name, '..') 

        subject_name = subfolders(i).name; % Extract subject name
        dti_filename = [subject_name, '_MD_C_native.mat'];
        tract_filename = [subject_name, '_MD_C_native_Tracts_DTI_Save.mat'];
        %save_segm_filename = [subject_name, '_left_segm.mat'];
        save_segm_filename = [subject_name, '_right_segm.mat'];
        
        % Check if tract file exists
        if exist(fullfile(input_path, subject_name, tract_filename), 'file') == 2
            % Call EDTI functions
            E_DTI_Load_DTI_data_from_mat_file(fullfile(input_path, subject_name), dti_filename);
            E_DTI_Load_Multiple_ROI(fullfile(input_path, subject_name));
            E_DTI_Load_Tracts(fullfile(input_path, subject_name), tract_filename);

            % for segmenting tracts
            E_DTI_Analyse_tracts_new(input_path_segm, save_segm_filename); 

            % Delete ROIs to delete previous ROIs and load the next ones
            % Don't forget to tick the all square!
            E_DTI_Delete_ROI('AND')
            E_DTI_Delete_ROI('AND')
            E_DTI_Delete_Tracts % Delete tracts in order to load the tracts of the next subject

            % Display success message
            fprintf('Tract segmentation for subject %s is successful.\n', subject_name);
        else
            % If tract file does not exist, print error message and add subject name to list
            fprintf('No tract file for subject %s found. Moving to next subject.\n', subject_name);
            no_tract_subjects = [no_tract_subjects; subject_name]; % Add subject name to list
            continue; % Move to next iteration
        end
    end
end


% Write the list of subjects without tracts to a text file
%output_file = 'H:\Marc_Pastur_pipeline\DTI_MODEL\Segmentation\Left\Missed_tracts.txt';
output_file = 'H:\Marc_Pastur_pipeline\DTI_MODEL\Segmentation\Right\Missed_tracts.txt';
fileID = fopen(output_file, 'w');
for i = 1:length(no_tract_subjects)
    fprintf(fileID, '%s\n', no_tract_subjects{i});
end

fclose(fileID);
