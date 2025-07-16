--Example entries for the researchlens_papersimilarity table containing pairs of papers with their similarity scores.
--You can use this SQL script to insert sample data into the researchlens_papersimilarity table.
--However, the tables is currently only filled with data but not used in the application for queries.
INSERT INTO public.researchlens_papersimilarity (id, similarity_score, source_paper_id, target_paper_id) VALUES (1, 0.9179244331454774, 20, 19);
