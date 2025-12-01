import React, { useEffect, useState, useCallback } from 'react';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Underline from '@tiptap/extension-underline';
import { TextStyle } from '@tiptap/extension-text-style';
import './TiptapEditor.scss';

/**
 * Tiptap Editor Component
 * Replaces the old EpicEditor/UberEditor
 */
const TiptapEditor = ({
    content = '',
    onChange,
    onBlur,
    placeholder = 'Start typing...',
    autoFocus = false,
    editable = true,
    minHeight = 180,
    showToolbar = true,
    className = '',
}) => {
    const [editorState, setEditorState] = useState(0); // Force re-render counter

    const editor = useEditor({
        extensions: [
            StarterKit.configure({
                heading: {
                    levels: [1, 2, 3, 4, 5, 6],
                },
                codeBlock: {
                    HTMLAttributes: {
                        class: 'hljs',
                    },
                },
            }),
            Underline,
            TextStyle,
        ],
        content,
        editable,
        autofocus: autoFocus,
        onUpdate: ({ editor }) => {
            const html = editor.getHTML();
            const text = editor.getText();
            if (onChange) {
                onChange(html, text, editor);
            }
        },
        onBlur: ({ editor }) => {
            if (onBlur) {
                onBlur(editor);
            }
        },
        onSelectionUpdate: () => {
            // Force re-render when selection changes (to update button states)
            setEditorState(prev => prev + 1);
        },
        immediatelyRender: false,
    });

    useEffect(() => {
        if (editor && content !== editor.getHTML()) {
            editor.commands.setContent(content);
        }
    }, [content]);

    useEffect(() => {
        if (editor) {
            editor.setEditable(editable);
        }
    }, [editable, editor]);

    const MenuBar = () => {
        if (!editor || !showToolbar) return null;

        return (
            <div className="tiptap-menubar">
                <div className="tiptap-menubar__buttons">
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleBold().run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('bold') ? 'is-active' : ''}
                        type="button"
                        title="Bold (Ctrl+B)"
                    >
                        <strong>B</strong>
                    </button>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleItalic().run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('italic') ? 'is-active' : ''}
                        type="button"
                        title="Italic (Ctrl+I)"
                    >
                        <em>I</em>
                    </button>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleUnderline().run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('underline') ? 'is-active' : ''}
                        type="button"
                        title="Underline (Ctrl+U)"
                    >
                        <u>U</u>
                    </button>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleStrike().run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('strike') ? 'is-active' : ''}
                        type="button"
                        title="Strikethrough"
                    >
                        <s>S</s>
                    </button>
                    <span className="tiptap-menubar__separator"></span>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleHeading({ level: 1 }).run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('heading', { level: 1 }) ? 'is-active' : ''}
                        type="button"
                        title="Heading 1"
                    >
                        H1
                    </button>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleHeading({ level: 2 }).run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('heading', { level: 2 }) ? 'is-active' : ''}
                        type="button"
                        title="Heading 2"
                    >
                        H2
                    </button>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleHeading({ level: 3 }).run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('heading', { level: 3 }) ? 'is-active' : ''}
                        type="button"
                        title="Heading 3"
                    >
                        H3
                    </button>
                    <span className="tiptap-menubar__separator"></span>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleBulletList().run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('bulletList') ? 'is-active' : ''}
                        type="button"
                        title="Bullet List"
                    >
                        •
                    </button>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleOrderedList().run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('orderedList') ? 'is-active' : ''}
                        type="button"
                        title="Numbered List"
                    >
                        1.
                    </button>
                    <span className="tiptap-menubar__separator"></span>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleCodeBlock().run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('codeBlock') ? 'is-active' : ''}
                        type="button"
                        title="Code Block"
                    >
                        {'</>'}
                    </button>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().toggleBlockquote().run();
                            setEditorState(prev => prev + 1);
                        }}
                        className={editor.isActive('blockquote') ? 'is-active' : ''}
                        type="button"
                        title="Quote"
                    >
                        "
                    </button>
                    <span className="tiptap-menubar__separator"></span>
                    <button
                        onMouseDown={(e) => {
                            e.preventDefault();
                            editor.chain().focus().setHorizontalRule().run();
                        }}
                        type="button"
                        title="Horizontal Rule"
                    >
                        —
                    </button>
                </div>
            </div>
        );
    };

    if (!editor) {
        return null;
    }

    return (
        <div className={`tiptap-editor-wrapper ${className}`}>
            <MenuBar />
            <div
                className="tiptap-editor-content"
                style={{ minHeight: `${minHeight}px` }}
            >
                <EditorContent editor={editor} />
            </div>
        </div>
    );
};

export default TiptapEditor;

