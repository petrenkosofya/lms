import React from 'react';
import ReactDOM from 'react-dom/client';
import { SimpleEditor } from './simple-editor';

/**
 * Initializes the editor for a textarea element
 * @param textarea - HTMLTextAreaElement to replace
 * @returns object with editor control methods
 */
export function initSimpleEditor(textarea: HTMLTextAreaElement) {
  // Hide the original textarea
  textarea.style.display = 'none';
  
  // Get initial content
  const initialContent = textarea.value || '';
  
  // Create container for React component
  const container = document.createElement('div');
  container.className = 'simple-editor-container';
  
  // Insert container after textarea
  textarea.parentNode?.insertBefore(container, textarea.nextSibling);
  
  // Create React root
  const root = ReactDOM.createRoot(container);
  
  // Store reference to editor for API
  let editorInstance: any = null;
  
  // Render component
  root.render(
    <SimpleEditor 
      content={initialContent}
      textarea={textarea}
      onReady={(editor) => {
        editorInstance = editor;
      }}
    />
  );
  
  // Return simple API
  return {
    getContent: () => textarea.value,
    setContent: (content: string) => editorInstance?.commands.setContent(content),
    focus: () => editorInstance?.commands.focus(),
    clear: () => editorInstance?.commands.clearContent(),
    destroy: () => {
      root.unmount();
      container.remove();
      textarea.style.display = '';
    },
    getEditor: () => editorInstance,
  };
}

// Export component for direct use
export { SimpleEditor } from './simple-editor';

