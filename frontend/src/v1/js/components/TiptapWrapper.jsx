import React from 'react';
import ReactDOM from 'react-dom/client';
import $ from 'jquery';
import TurndownService from 'turndown';
import { marked } from 'marked';
import TiptapEditor from './TiptapEditor';
import { getLocalStorageKey, createNotification } from '../utils';
import hljs from 'highlight.js';
import _escape from 'lodash-es/escape';
import _unescape from 'lodash-es/unescape';

// Initialize Turndown service for HTML to Markdown conversion
const turndownService = new TurndownService({
  headingStyle: 'atx',
  codeBlockStyle: 'fenced',
  bulletListMarker: '-',
  emDelimiter: '*',
});

// Configure marked for markdown to HTML conversion
marked.setOptions({
  breaks: true,
  gfm: true,
});

/**
 * TiptapWrapper - jQuery-compatible wrapper for Tiptap editor
 * Replaces UberEditor to maintain backwards compatibility
 */
export default class TiptapWrapper {
  static instances = new Map();

  /**
   * Initialize Tiptap editor for a textarea
   * @param {HTMLTextAreaElement} textarea 
   * @returns {Object} Editor instance
   */
  static init(textarea) {
    const $textarea = $(textarea);
    const $container = $('<div class="tiptap-container"/>').insertAfter($textarea);

    const autoSaveEnabled = $textarea.data('local-persist') === true;
    const showHelpFormatting = $textarea.data('helper-formatting') === true;
    const shouldFocus = $textarea.prop('autofocus');
    const minHeight = 180;

    // Hide original textarea
    $textarea.hide();
    $textarea.removeProp('required');

    // Hide formatting helper if present
    if (showHelpFormatting && $textarea.attr('id')) {
      $(`#hint_${$textarea.attr('id')}`).hide();
    }

    // Get initial content from textarea and convert markdown to HTML for Tiptap
    const initialMarkdown = $textarea.val() || '';
    let initialContent = '';
    if (initialMarkdown) {
      try {
        initialContent = marked.parse(initialMarkdown);
      } catch (e) {
        console.error('Failed to parse markdown:', e);
        initialContent = initialMarkdown;
      }
    }

    // Auto-save setup
    let autoSaveKey = null;
    let autoSaveTimeout = null;
    if (autoSaveEnabled) {
      if (!textarea.name) {
        console.error('Missing attr `name` for textarea. Text restore will be buggy.');
      }
      autoSaveKey = getLocalStorageKey(textarea);

      // Try to restore from localStorage
      const saved = localStorage.getItem(autoSaveKey);
      if (saved) {
        try {
          const data = JSON.parse(saved);
          if (data.content) {
            $textarea.val(data.content);
          }
        } catch (e) {
          console.error('Failed to restore from localStorage:', e);
        }
      }
    }

    const editorProps = {
      content: initialContent,
      autoFocus: shouldFocus,
      minHeight,
      showToolbar: true,
      placeholder: $textarea.attr('placeholder') || 'Start typing...',
      onChange: (html, text, editor) => {
        // Convert HTML to Markdown for backend compatibility
        let markdown;
        try {
          // Handle empty content
          if (!html || html === '<p></p>' || html.trim() === '') {
            markdown = '';
          } else {
            markdown = turndownService.turndown(html);
          }
        } catch (e) {
          console.error('Failed to convert HTML to markdown:', e);
          markdown = text; // Fallback to plain text
        }

        // Update textarea value with markdown
        $textarea.val(markdown);
        $textarea.trigger('change');

        // Auto-save
        if (autoSaveEnabled && autoSaveKey) {
          clearTimeout(autoSaveTimeout);
          autoSaveTimeout = setTimeout(() => {
            try {
              localStorage.setItem(autoSaveKey, JSON.stringify({
                content: markdown,
                modified: new Date().toISOString()
              }));
            } catch (e) {
              console.error('Failed to save to localStorage:', e);
            }
          }, 200);
        }
      },
    };

    // Create React root and render
    const root = ReactDOM.createRoot($container[0]);
    root.render(<TiptapEditor {...editorProps} />);

    // Create editor instance object for backwards compatibility
    const editorInstance = {
      _container: $container[0],
      _textarea: textarea,
      _root: root,
      _autoSaveKey: autoSaveKey,

      focus() {
        // Focus is handled by Tiptap internally
        $container.find('.ProseMirror').focus();
      },

      getElement(name) {
        if (name === 'editor') {
          return $container.find('.ProseMirror')[0];
        }
        return $container[0];
      },

      reflow() {
        // Tiptap handles reflow automatically
      },

      on(event, callback) {
        // Event handling compatibility
        if (event === 'preview') {
          // Preview is now handled internally
        }
      },

      emit(event) {
        // Event emitting compatibility
      },

      exportFile() {
        return $textarea.val();
      },

      remove(key) {
        if (key) {
          localStorage.removeItem(key);
        }
      },

      unload() {
        if (this._root) {
          this._root.unmount();
        }
        $container.remove();
        $textarea.show();
      }
    };

    // Handle Ctrl+Enter for quick send
    if ($textarea[0].getAttribute('data-quicksend') === 'true') {
      $container.on('keydown', function (e) {
        if (e.keyCode === 13 && (e.metaKey || e.ctrlKey)) {
          $textarea.closest('form').submit();
        }
      });
    }

    // Restore label behavior
    $('label[for=id_' + textarea.name + ']').click(function () {
      editorInstance.focus();
    });

    // Store instance
    TiptapWrapper.instances.set(textarea, editorInstance);

    return editorInstance;
  }

  /**
   * Preload required scripts (MathJax, etc.)
   */
  static preload(callback = function () { }) {
    $('body').addClass('tex2jax_ignore');
    const scripts = [
      window.__CSC__.config.JS_SRC.MATHJAX,
    ];
    const deferred = $.Deferred();
    let chained = deferred;
    $.each(scripts, function (i, url) {
      chained = chained.then(function () {
        return $.ajax({
          url: url,
          dataType: 'script',
          cache: true
        });
      });
    });
    chained.done(callback);
    deferred.resolve();
  }

  /**
   * Render markdown content with MathJax and syntax highlighting
   */
  static render(target) {
    if (window.MathJax && window.MathJax.Hub) {
      MathJax.Hub.Queue([
        'Typeset',
        MathJax.Hub,
        target,
        function () {
          $(target)
            .find('pre')
            .addClass('hljs')
            .find('code')
            .each(function (i, block) {
              const t = block.innerHTML;
              block.innerHTML = _escape(_unescape(_unescape(t)));
              hljs.highlightElement(block);
            });
        }
      ]);
    } else {
      // If MathJax not loaded, just do syntax highlighting
      $(target)
        .find('pre')
        .addClass('hljs')
        .find('code')
        .each(function (i, block) {
          const t = block.innerHTML;
          block.innerHTML = _escape(_unescape(_unescape(t)));
          hljs.highlightElement(block);
        });
    }
  }

  /**
   * Reflow editor when tab is toggled
   */
  static reflowOnTabToggle(e) {
    const activeTab = $($(e.target).attr('href'));
    TiptapWrapper.reflowEditor(activeTab);
  }

  /**
   * Reflow editors in a specific wrapper
   */
  static reflowEditor(editorWrapper) {
    // Tiptap handles this automatically, but we keep for compatibility
    const $containers = editorWrapper.find('.tiptap-container');
    $containers.each(function () {
      // Trigger reflow if needed
      $(this).find('.ProseMirror').trigger('focus').trigger('blur');
    });
  }

  /**
   * Clean old localStorage entries
   */
  static cleanLocalStorage(textareas) {
    if (textareas.length > 0 && window.hasOwnProperty('localStorage')) {
      const now = new Date();
      Object.keys(localStorage).forEach(key => {
        if (key.startsWith('tiptap-') || key.startsWith('epiceditor-')) {
          try {
            const data = JSON.parse(localStorage.getItem(key));
            if (data.modified) {
              const modified = new Date(data.modified);
              const hoursOld = (now - modified) / (1000 * 60 * 60);
              if (hoursOld > 24) {
                localStorage.removeItem(key);
              }
            }
          } catch (e) {
            // Invalid data, remove it
            localStorage.removeItem(key);
          }
        }
      });
    }
  }

  /**
   * Get editor instance for a textarea
   */
  static getInstance(textarea) {
    return TiptapWrapper.instances.get(textarea);
  }
}

