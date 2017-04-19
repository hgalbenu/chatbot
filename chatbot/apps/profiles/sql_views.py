# These query strings can be used inside Alembic migrations to easily re-create views if any data model changes
# which would affect the view are performed.

USER_WITH_EXTERNAL_LINKS_QUERY = \
    'CREATE OR REPLACE VIEW user_with_external_links AS SELECT *, ' \
    '\'https://finguidekirkwood.herokuapp.com/profile/\'||id AS kirkwood_url, ' \
    '\'https://finguidekirkwood.herokuapp.com/profile-edit/\'||id AS kirkwood_edit_url, ' \
    '("firstName" is not null and "firstName" != \'\')::int + ' \
    '("questionConsultation" is not null and "questionConsultation" != \'\')::int + ' \
    '("email" is not null and "email" != \'\')::int + ' \
    '("situationDetail" is not null and "situationDetail" != \'\')::int + ' \
    '("is_married" is not null)::int + ' \
    '("employment_status" is not null and "employment_status" != \'\')::int + ' \
    '("additional_income" is not null)::int + ' \
    '("additional_income_amount" is not null and "additional_income_amount" != \'\')::int + ' \
    '("additional_income_consistent" is not null)::int + ' \
    '("state" is not null and "state" != \'\')::int + ' \
    '("ownHome" is not null and "ownHome" != \'\')::int + ' \
    '("homeEquity" is not null and "homeEquity" != \'\')::int + ' \
    '("houseHoldSize" is not null and "houseHoldSize" != \'\')::int + ' \
    '("totalDebt" is not null and "totalDebt" != \'\')::int + ' \
    '("basic_hardship" is not null and "basic_hardship" != \'\')::int + ' \
    '("monthlyDebtPayments" is not null and "monthlyDebtPayments" != \'\')::int + ' \
    '("credit_score_importance" is not null and "credit_score_importance" != \'\')::int + ' \
    '("needs_future_student_loan" is not null and "needs_future_student_loan" != \'\')::int + ' \
    '("needs_future_auto_loan" is not null and "needs_future_auto_loan" != \'\')::int + ' \
    '("needs_future_mortgage" is not null and "needs_future_mortgage" != \'\')::int + ' \
    '("phoneOrEmail" is not null and "phoneOrEmail" != \'\')::int + ' \
    '("phone" is not null and "phone" != \'\')::int + ' \
    '("revenue_potential" is not null)::int + ' \
    '("expert_note" is not null and "expert_note" != \'\')::int + ' \
    '("current_job_id" is not null)::int + ' \
    '("current_debt_id" is not null)::int AS profile_completeness_score ' \
    'FROM public.\"profiles_userprofile\";'
