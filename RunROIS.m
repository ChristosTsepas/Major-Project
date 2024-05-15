% This script is for creating SEED and AND ROIs
% Calls iternally the scripts/functio s Create_ROIs and Create_Segm_ROI

%folder_path = 'H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Tract_analysis\Left';
folder_path = 'H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Tract_analysis\Right';
subfolders = dir(fullfile(folder_path, '*'));

for i = 1:length(subfolders)
    if subfolders(i).isdir && ~strcmp(subfolders(i).name, '.') && ~strcmp(subfolders(i).name, '..')
        subfolder_path = fullfile(folder_path, subfolders(i).name);
        disp(['Creating ROIs for ' subfolders(i).name]);
        Create_ROIs(subfolder_path);
    end
end



%segm = 'H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Segmentation\Left';
segm = 'H:\Marc_Pastur_pipeline\DTI_MODEL\ROI_generation\Segmentation\Right';

sub = dir(fullfile(segm, '*'));
for i = 1:length(sub)
    if  sub(i).isdir && ~strcmp(sub(i).name, '.') && ~strcmp(sub(i).name, '..')
            sub_path = fullfile(segm, sub(i).name);
            Create_segm_ROI(sub_path);
            fprintf('AND ROIs for subject %s for segmentation are loaded, column positions swapped, and saved successfully. \n', sub(i).name);
        
    end
end


