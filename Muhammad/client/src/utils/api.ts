const API_BASE_URL = 'http://localhost:8000';

export interface UploadedFile {
  filename: string;
  status: 'uploaded' | 'skipped';
  path?: string;
  size?: number;
  reason?: string;
}

export interface UploadResponse {
  source_files: UploadedFile[];
  target_files: UploadedFile[];
  user_id: string;
}

export const uploadFiles = async (sourceFiles: File[], targetFiles: File[]): Promise<UploadResponse> => {
  const formData = new FormData();
  
  // Append source files with the correct field name
  sourceFiles.forEach((file) => {
    // Create a new File object to ensure the correct filename is sent
    const fileWithName = new File([file], file.name, { type: file.type });
    formData.append('source_files', fileWithName, file.name);
  });
  
  // Append target files with the correct field name
  targetFiles.forEach((file) => {
    // Create a new File object to ensure the correct filename is sent
    const fileWithName = new File([file], file.name, { type: file.type });
    formData.append('target_files', fileWithName, file.name);
  });

  // Generate a new user ID for this session
  const userId = localStorage.getItem('userId') || "fbdb3c39-e91e-49d9-b142-81e935f077c9"
  // Append user ID as form data
  formData.append('user_id', userId);

  try {
    const response = await fetch(`${API_BASE_URL}/api/upload-files`, {
      method: 'POST',
      body: formData,
      // Note: Don't set Content-Type header, let the browser set it with the boundary
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || data.error || 'Failed to upload files');
    }

    return data as UploadResponse;
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
};
