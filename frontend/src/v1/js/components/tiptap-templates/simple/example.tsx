/**
 * Пример использования SimpleEditor с алиасом @
 * 
 * Этот файл показывает, как правильно импортировать и использовать
 * SimpleEditor в React-приложении
 */

import React, { useState } from 'react';
import { SimpleEditor } from '@/components/tiptap-templates/simple/simple-editor';

/**
 * Простой пример - базовое использование
 */
export function BasicExample() {
  return <SimpleEditor />;
}

/**
 * Пример с контролируемым состоянием
 */
export function ControlledExample() {
  const [content, setContent] = useState('<p>Начальный текст</p>');

  const handleChange = (newContent: string) => {
    setContent(newContent);
    console.log('Содержимое изменено:', newContent);
  };

  return (
    <div>
      <SimpleEditor 
        content={content}
        onChange={handleChange}
        placeholder="Введите текст..."
      />
      
      <div style={{ marginTop: '20px' }}>
        <h3>Предпросмотр содержимого:</h3>
        <div dangerouslySetInnerHTML={{ __html: content }} />
      </div>
    </div>
  );
}

/**
 * Пример с сохранением в форму
 */
export function FormExample() {
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);
  const [savedContent, setSavedContent] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const content = formData.get('content') as string;
    setSavedContent(content);
    alert('Форма отправлена!');
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        ref={textareaRef}
        name="content"
        style={{ display: 'none' }}
      />
      
      <SimpleEditor 
        textarea={textareaRef.current || undefined}
        placeholder="Напишите что-нибудь..."
      />
      
      <button type="submit" style={{ marginTop: '10px' }}>
        Отправить
      </button>
      
      {savedContent && (
        <div style={{ marginTop: '20px' }}>
          <h3>Сохраненное содержимое:</h3>
          <pre>{savedContent}</pre>
        </div>
      )}
    </form>
  );
}

/**
 * Пример с доступом к API редактора
 */
export function EditorAPIExample() {
  const [editor, setEditor] = useState<any>(null);

  const handleClear = () => {
    if (editor) {
      editor.commands.clearContent();
    }
  };

  const handleInsertText = () => {
    if (editor) {
      editor.commands.insertContent('<p><strong>Вставленный текст!</strong></p>');
    }
  };

  return (
    <div>
      <SimpleEditor 
        onReady={(editorInstance) => setEditor(editorInstance)}
      />
      
      <div style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
        <button onClick={handleClear}>Очистить</button>
        <button onClick={handleInsertText}>Вставить текст</button>
      </div>
    </div>
  );
}

/**
 * Главный компонент-пример со всеми вариантами использования
 */
export default function App() {
  const [activeTab, setActiveTab] = useState<'basic' | 'controlled' | 'form' | 'api'>('basic');

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Примеры использования SimpleEditor</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <button onClick={() => setActiveTab('basic')}>Базовый</button>
        <button onClick={() => setActiveTab('controlled')}>Контролируемый</button>
        <button onClick={() => setActiveTab('form')}>Форма</button>
        <button onClick={() => setActiveTab('api')}>API</button>
      </div>

      {activeTab === 'basic' && (
        <div>
          <h2>Базовый пример</h2>
          <BasicExample />
        </div>
      )}

      {activeTab === 'controlled' && (
        <div>
          <h2>Контролируемое состояние</h2>
          <ControlledExample />
        </div>
      )}

      {activeTab === 'form' && (
        <div>
          <h2>Интеграция с формой</h2>
          <FormExample />
        </div>
      )}

      {activeTab === 'api' && (
        <div>
          <h2>Использование API</h2>
          <EditorAPIExample />
        </div>
      )}
    </div>
  );
}

/**
 * Как использовать этот компонент:
 * 
 * 1. В Django шаблоне:
 *    <div data-component="SimpleEditorExample"></div>
 * 
 * 2. В React приложении:
 *    import App from '@/components/tiptap-templates/simple/example';
 *    <App />
 * 
 * 3. Программно:
 *    import { initSimpleEditor } from '@/components/tiptap-templates/simple';
 *    const textarea = document.querySelector('textarea.ubereditor');
 *    initSimpleEditor(textarea);
 */

