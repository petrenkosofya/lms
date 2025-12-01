import $ from 'jquery';

import TiptapWrapper from 'components/TiptapWrapper';
import { createNotification, getCSRFToken } from '../utils';
import ky from 'ky'

const commentButton = $('#add-comment');
const commentForm = $('#comment-form-wrapper');
const solutionButton = $('#add-solution');
const solutionForm = $('#solution-form-wrapper');
const jbaTab = $('#tab-jba');
const jbaTabContent = $('#tab-content-jba');
const jbaCourseTutorial = $('#jba-course-tutorial');
const jbaMarketplaceLink = $('#jba-marketplace-link');
const jbaUpdateResultsBtn = $('#jba-update-results-btn');

const fn = {
  initCommentForm: function () {
    commentButton.on('click', function () {
      commentForm.removeClass('hidden');
      TiptapWrapper.reflowEditor(commentForm);
      $(this).addClass('active');
      if (solutionForm.length > 0) {
        solutionForm.addClass('hidden');
        solutionButton.removeClass('active');
      } else if (jbaTabContent.length > 0) {
        jbaTabContent.addClass('hidden');
        jbaTab.removeClass('active');
      }
    });
  },

  initSolutionForm: function () {
    if (solutionForm.length > 0) {
      solutionButton.on('click', function () {
        solutionForm.removeClass('hidden');
        TiptapWrapper.reflowEditor(solutionForm);
        $(this).addClass('active');
        commentForm.addClass('hidden');
        commentButton.removeClass('active');
      });
    }
  },

  initJbaTab: function () {
    if (jbaTabContent.length == 0) {
      return
    }
    jbaTab.click(() => {
      jbaTabContent.removeClass('hidden');
      jbaTab.addClass('active');

      commentForm.addClass('hidden');
      commentButton.removeClass('active');
    });

    jbaMarketplaceLink.attr('href', jbaCourseTutorial.data('marketplaceLink'))

    jbaUpdateResultsBtn.click(() => {
      const studentAssignmentId = jbaUpdateResultsBtn.data('studentAssignmentId')
      jbaUpdateResultsBtn.prop('disabled', true)
      ky.post(`/api/v1/study/assignments/${studentAssignmentId}/update_jba_progress`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken() },
      }).then(() => {
        location.reload()
      }).catch(() => {
        createNotification('Failed to update the IDE course results', 'error')
        jbaUpdateResultsBtn.prop('disabled', false)
      })
    })
  },

  initCommentModal: function () {
    $(document).on('click', '.__edit', function (e) {
      e.preventDefault();
      const $editLink = $(this);
      const editUrl = $editLink.attr('href');
      const $commentPanel = $editLink.closest('.assignment-submission');

      if ($commentPanel.length === 0) {
        console.error('Comment panel not found');
        return;
      }

      const $panelBody = $commentPanel.find('.panel-body');
      const $ubertextDiv = $panelBody.find('.ubertext');
      const commentId = $commentPanel.data('id');

      if ($commentPanel.hasClass('editing')) {
        return;
      }

      $editLink.hide();
      $commentPanel.addClass('editing');

      const $loadingIndicator = $('<div class="inline-editor-loading"><i class="fa fa-spinner fa-spin"></i> Loading editor...</div>');
      if ($ubertextDiv.length > 0) {
        $ubertextDiv.after($loadingIndicator);
      } else {
        $panelBody.append($loadingIndicator);
      }

      $.get(editUrl)
        .done(function (data) {
          $loadingIndicator.remove();

          const $editorContainer = $('<div class="inline-comment-editor"></div>');
          const $formWrapper = $('<div class="inline-editor-form"></div>').html(data);

          $formWrapper.find('.modal-footer').remove();

          const $helpText = $('<div class="text-muted mb-10"><small><i class="fa fa-info-circle"></i> Press Esc to cancel editing</small></div>');

          const $buttonBar = $('<div class="inline-editor-buttons"></div>');
          const $saveBtn = $('<button type="button" class="btn btn-primary btn-sm">Save</button>');
          const $cancelBtn = $('<button type="button" class="btn btn-default btn-sm">Cancel</button>');
          $buttonBar.append($cancelBtn).append($saveBtn);

          $editorContainer.append($helpText).append($formWrapper).append($buttonBar);

          if ($ubertextDiv.length > 0) {
            $ubertextDiv.hide();
            $ubertextDiv.after($editorContainer);
          } else {
            $panelBody.append($editorContainer);
          }

          const handleEscape = function (e) {
            if (!$commentPanel.hasClass('editing')) {
              return;
            }
            if (e.key === 'Escape' || e.keyCode === 27) {
              e.preventDefault();
              e.stopPropagation();
              fn.cancelInlineEdit($commentPanel, $editorContainer, $ubertextDiv, $editLink);
              return false;
            }
          };

          $(document).on('keydown.inline-edit', handleEscape);
          $editorContainer.on('keydown.escape-edit', handleEscape);

          $cancelBtn.on('click', function () {
            fn.cancelInlineEdit($commentPanel, $editorContainer, $ubertextDiv, $editLink);
          });

          $saveBtn.on('click', function () {
            fn.saveInlineEdit($commentPanel, $editorContainer, $ubertextDiv, $editLink, $formWrapper, commentId);
          });

          setTimeout(() => {
            const textarea = $editorContainer.find('textarea').get(0);
            if (textarea) {
              const editor = TiptapWrapper.init(textarea);
              $editorContainer.data('editor', editor);

              try {
                const editorDoc = editor.getElement('editor');
                if (editorDoc && editorDoc.body) {
                  $(editorDoc.body).on('keydown.escape-edit-iframe', function (e) {
                    if (e.key === 'Escape' || e.keyCode === 27) {
                      e.preventDefault();
                      e.stopPropagation();
                      fn.cancelInlineEdit($commentPanel, $editorContainer, $ubertextDiv, $editLink);
                      return false;
                    }
                  });

                  $(editorDoc).on('keydown.escape-edit-iframe', function (e) {
                    if (e.key === 'Escape' || e.keyCode === 27) {
                      e.preventDefault();
                      e.stopPropagation();
                      fn.cancelInlineEdit($commentPanel, $editorContainer, $ubertextDiv, $editLink);
                      return false;
                    }
                  });
                }
              } catch (e) {
                console.debug('Could not attach escape handler to editor iframe:', e);
              }

              editor.focus();
            }
          }, 100);
        })
        .fail(function (data) {
          $loadingIndicator.remove();
          $commentPanel.removeClass('editing');
          $editLink.show();
          if (data.status === 403) {
            const msg = 'Access denied. Probably, the time to edit the comment has expired.';
            createNotification(msg, 'error');
            $editLink.remove();
          } else {
            createNotification('Failed to load edit form', 'error');
          }
        });
    });
  },

  cancelInlineEdit: function ($commentPanel, $editorContainer, $ubertextDiv, $editLink) {
    $(document).off('keydown.inline-edit');
    $editorContainer.off('keydown.escape-edit');

    try {
      const editor = $editorContainer.data('editor');
      if (editor) {
        const editorDoc = editor.getElement('editor');
        if (editorDoc) {
          $(editorDoc).off('keydown.escape-edit-iframe');
          if (editorDoc.body) {
            $(editorDoc.body).off('keydown.escape-edit-iframe');
          }
        }
      }
    } catch (e) {
    }

    $editorContainer.fadeOut(200, function () {
      $editorContainer.remove();
      if ($ubertextDiv.length > 0) {
        $ubertextDiv.fadeIn(200);
      }
      $editLink.show();
      $commentPanel.removeClass('editing');
    });
  },

  saveInlineEdit: function ($commentPanel, $editorContainer, $ubertextDiv, $editLink, $formWrapper, commentId) {
    const $form = $formWrapper.find('form');
    const $saveBtn = $editorContainer.find('.btn-primary');

    $saveBtn.prop('disabled', true).text('Saving...');

    $.ajax({
      url: $form.attr('action'),
      type: 'POST',
      data: $form.serialize(),
    })
      .done(function (json) {
        if (json.success === 1) {
          $(document).off('keydown.inline-edit');
          $editorContainer.off('keydown.escape-edit');

          if ($ubertextDiv.length > 0) {
            $ubertextDiv.html(json.html);
            TiptapWrapper.render($ubertextDiv.get(0));
          } else {
            const $panelBody = $commentPanel.find('.panel-body');
            const $newUbertext = $('<div class="ubertext"></div>').html(json.html);
            $panelBody.append($newUbertext);
            TiptapWrapper.render($newUbertext.get(0));
          }

          const $dateSpan = $commentPanel.find('.assignment-submission__date');
          if (json.is_edited && json.modified) {
            let $editedBadge = $dateSpan.find('.comment-edited-badge');
            if ($editedBadge.length === 0) {
              $editedBadge = $('<span class="comment-edited-badge" title="Edited: ' + json.modified + '"><i class="fa fa-pencil"></i> edited</span>');
              if ($dateSpan.text().trim()) {
                $dateSpan.append(' ');
              }
              $dateSpan.append($editedBadge);
            } else {
              $editedBadge.attr('title', 'Edited: ' + json.modified);
            }
          }

          $editorContainer.fadeOut(200, function () {
            $editorContainer.remove();
            if ($ubertextDiv.length > 0) {
              $ubertextDiv.fadeIn(200);
            }
            $editLink.show();
            $commentPanel.removeClass('editing');
          });

          createNotification('Comment updated successfully');
        } else {
          $saveBtn.prop('disabled', false).text('Save');
          createNotification('Failed to update the comment', 'error');
        }
      })
      .fail(function () {
        $saveBtn.prop('disabled', false).text('Save');
        createNotification('Failed to update the comment', 'error');
      });
  },
};

export function launch() {
  fn.initCommentForm();
  fn.initSolutionForm();
  fn.initJbaTab();
  fn.initCommentModal();
}

export function initInlineCommentEditing() {
  fn.initCommentModal();
}
