let fileStore: {
    sourceFiles: File[];
    targetFiles: File[];
  } = {
    sourceFiles: [],
    targetFiles: []
  };
  
  export const setFiles = (sourceFiles: File[], targetFiles: File[]) => {
    fileStore.sourceFiles = sourceFiles;
    fileStore.targetFiles = targetFiles;
  };
  
  export const getFiles = () => {
    return {
      sourceFiles: fileStore.sourceFiles,
      targetFiles: fileStore.targetFiles
    };
  };
  
  export const clearFiles = () => {
    fileStore.sourceFiles = [];
    fileStore.targetFiles = [];
  };