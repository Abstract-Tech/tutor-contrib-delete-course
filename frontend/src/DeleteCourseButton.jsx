/* eslint-disable no-alert */
import React, { useEffect, useMemo, useState } from 'react';
import { useIntl } from '@edx/frontend-platform/i18n';
import  messages  from './i18n/messages';
import {
  ActionRow,
  AlertModal,
  Button,
  Form,
} from '@openedx/paragon';
import { canDeleteCourse, deleteCourse } from './api';


const getErrorMessage = (error, intl) => (
  error?.response?.data?.error
  || error?.response?.data?.message
  || error?.message
  || intl.formatMessage(messages.failedToDeleteCourse)
);

const extractCourseIdFromLocation = () => {
  if (typeof window === 'undefined') {
    return '';
  }

  const href = window.location?.href || '';
  const pathname = window.location?.pathname || '';
  const search = window.location?.search || '';
  const candidates = [href, pathname, search];

  for (const value of candidates) {
    const match = value.match(/course-v1:[^/?&#]+/);
    if (match?.[0]) {
      try {
        return decodeURIComponent(match[0]);
      } catch {
        return match[0];
      }
    }
  }

  return '';
};

const DeleteCourseButton = ({ courseId, courseKey, courseKeyString, redirectPath = '/authoring/home' }) => {
  const intl = useIntl();
  const [isDeleting, setIsDeleting] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [reason, setReason] = useState('');
  const [confirmCourseId, setConfirmCourseId] = useState('');
  const [canRenderDelete, setCanRenderDelete] = useState(false);

  const resolvedCourseId = useMemo(() => (
    courseId
    || courseKey
    || courseKeyString
    || extractCourseIdFromLocation()
    || ''
  ).trim(), [courseId, courseKey, courseKeyString]);

  const isCourseIdConfirmed = confirmCourseId.trim() === resolvedCourseId;

  useEffect(() => {
    let isMounted = true;

    const loadPermission = async () => {
      if (!resolvedCourseId) {
        if (isMounted) {
          setCanRenderDelete(false);
        }
        return;
      }

      try {
        await canDeleteCourse(resolvedCourseId);
        if (isMounted) {
          setCanRenderDelete(true);
        }
      } catch {
        if (isMounted) {
          setCanRenderDelete(false);
        }
      }
    };

    loadPermission();
    return () => {
      isMounted = false;
    };
  }, [resolvedCourseId]);

  const handleDeleteCourse = async () => {
    if (!resolvedCourseId) {
      window.alert(intl.formatMessage(messages.unableToResolveCourseId));
      return;
    }

    if (!isCourseIdConfirmed) {
      return;
    }

    setIsDeleting(true);
    try {
      await deleteCourse(resolvedCourseId, {
        reason: reason.trim(),
      });
      setIsConfirmOpen(false);
      setReason('');
      setConfirmCourseId('');
      window.location.assign(redirectPath);
    } catch (error) {
      window.alert(getErrorMessage(error, intl));
    } finally {
      setIsDeleting(false);
    }
  };

  if (!canRenderDelete) {
    return null;
  }

  return (
    <>
      <Button
        variant="danger"
        onClick={() => setIsConfirmOpen(true)}
        disabled={isDeleting}
      >
        {isDeleting ? intl.formatMessage(messages.deletingButton) : intl.formatMessage(messages.deleteCourseButton)}
      </Button>
      <AlertModal
        title={intl.formatMessage(messages.modalTitle)}
        variant="danger"
        isOpen={isConfirmOpen}
        onClose={() => {
          if (!isDeleting) {
            setIsConfirmOpen(false);
            setConfirmCourseId('');
          }
        }}
        footerNode={(
          <ActionRow>
            <Button
              variant="tertiary"
              disabled={isDeleting}
              onClick={() => setIsConfirmOpen(false)}
            >
              {intl.formatMessage(messages.cancelButton)}
            </Button>
            <Button
              variant="danger"
              disabled={isDeleting || !isCourseIdConfirmed}
              onClick={handleDeleteCourse}
            >
              {isDeleting ? intl.formatMessage(messages.deletingButton) : intl.formatMessage(messages.deleteCourseButton)}
            </Button>
          </ActionRow>
        )}
      >
        <p className="mb-3">{intl.formatMessage(messages.modalMessage)}</p>
        <Form.Group controlId="delete-course-id">
          <Form.Label>{intl.formatMessage(messages.courseIdLabel)}</Form.Label>
          <Form.Control value={resolvedCourseId} readOnly />
        </Form.Group>
        <Form.Group controlId="delete-course-id-confirmation">
          <Form.Label>{intl.formatMessage(messages.courseIdConfirmLabel)}</Form.Label>
          <Form.Control
            type="text"
            value={confirmCourseId}
            placeholder={intl.formatMessage(messages.courseIdConfirmPlaceholder)}
            onChange={(event) => setConfirmCourseId(event.target.value)}
          />
        </Form.Group>
        <Form.Group controlId="delete-course-reason">
          <Form.Label>{intl.formatMessage(messages.reasonPrompt)}</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            value={reason}
            onChange={(event) => setReason(event.target.value)}
          />
        </Form.Group>
      </AlertModal>
    </>
  );
};

export default DeleteCourseButton;
