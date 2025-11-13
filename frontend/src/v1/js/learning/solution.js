import $ from 'jquery';

import { initSimpleEditor } from 'components/tiptap-templates/simple/index';
import { createNotification, getCSRFToken } from '../utils';
import ky from 'ky'

const comment = $('.assignment-comment');
const modalFormWrapper = $('#update-comment-model-form');

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
    modalFormWrapper.modal({
      show: false,
    });
    
    // Show modal
    $('.__edit', comment).click(function (e) {
      e.preventDefault();
      const $this = $(this);
      $.get(this.href, function (data) {
        modalFormWrapper.css('opacity', '1');
        $('.inner', modalFormWrapper).html(data);
        
        // Initialize editor for textarea in loaded content
        const textarea = $('.inner', modalFormWrapper).find('textarea').get(0);
        if (textarea) {
          initSimpleEditor(textarea);
        }
        
        modalFormWrapper.modal('show');
      }).fail(function (data) {
        if (data.status === 403) {
          const msg = 'Access denied. Probably, the time to edit the comment has expired.';
          createNotification(msg, 'error');
          $this.remove();
        }
      });
    });

    modalFormWrapper.on('submit', 'form', fn.onSubmitCommentModalForm);
  },

  onSubmitCommentModalForm: function (event) {
    event.preventDefault();
    let form = event.target;
    // TODO: validate empty comment here
    $.ajax({
      url: form.action,
      type: 'POST',
      data: $(form).serialize(),
    })
      .done(function (json) {
        if (json.success === 1) {
          modalFormWrapper.modal('hide');
          let target = comment.filter(function () {
            return $(this).data('id') == json.id;
          });
          const textElement = $('.ubertext', target);
          textElement.html(json.html);
          // Highlight code in updated content
          textElement.find('pre code').each(function(i, block) {
            import('highlight.js').then(hljs => hljs.default.highlightElement(block));
          });
          createNotification('Comment changed');
        } else {
          createNotification('Failed to update the comment', 'error');
        }
      })
      .fail(function () {
        createNotification('Failed to update the comment', 'error');
      });
    return false;
  },
};

export function launch() {
  fn.initCommentForm();
  fn.initSolutionForm();
  fn.initJbaTab();
  fn.initCommentModal();
}
