-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Create profiles table
create table if not exists profiles (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  technical_skills text[] default '{}',
  projects text[] default '{}',
  ai_expertise text[] default '{}',
  mentoring_preferences text not null,
  collaboration_interests text[] default '{}',
  portfolio_url text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Create text search index for better search performance
create index if not exists profiles_name_idx on profiles using gin (to_tsvector('english', name));
create index if not exists profiles_mentoring_idx on profiles using gin (to_tsvector('english', mentoring_preferences)); 